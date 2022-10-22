#!/usr/bin/python3
""" Module containing Place View """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage, storage_t
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """ Retrieves the list of all Place objects of a City.

        Args:
            city_id (str): The UUID4 string representing a City object.

        Returns:
            List of dictionaries representing Place objects in JSON format.
            Raise 404 error if `city_id` is not linked to any City object.
    """
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        abort(404)
    places = [place.to_dict() for place in city_obj.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Retrieves a Place object based on `place_id`.

    Args:
        place_id (str): The UUID4 string representing a Place object.

    Returns:
        Dictionary represention of a Place object in JSON format.
        Raise 404 error if `place_id` is not linked to any Place object.
    """
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    return jsonify(place_obj.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a Place object based on `place_id`.

    Args:
        place_id (str): The UUID4 string representing a Place object.

    Returns:
        Returns an empty dictionary with the status code 200.
        Raise 404 error if `place_id` is not linked to any Place object.
    """
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    place_obj.delete()
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def add_place(city_id):
    """ Creates a Place object using `city_id` and HTTP body request fields.

    Args:
        city_id (str): The UUID4 string representing a City object.

    Returns:
        Returns the new Place object as a  dictionary in JSON format
        with the status code 200.
        Raise 404 error if `state_id` is not linked to any State object.
    """
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        abort(404)
    if request.json is None:
        return "Not a JSON", 400
    fields = request.get_json()
    if fields.get('user_id') is None:
        return "Missing user_id", 400
    user_obj = storage.get("User", fields['user_id'])
    if user_obj is None:
        abort(404)
    if fields.get('name') is None:
        return "Missing name", 400
    fields['city_id'] = city_id
    new_place = Place(**fields)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def edit_place(place_id):
    """ Edit a Place object using `place_id` and HTTP body request fields.

    Args:
        place_id (str): The UUID4 string representing a Place object.

    Returns:
        Returns the Place object as a  dictionary in JSON format with the
        status code 200.
        Raise 404 error if `place_id` is not linked to any Place object.
    """
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    if request.json is None:
        return "Not a JSON", 400
    fields = request.get_json()
    for key in fields:
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'update_at']:
            if hasattr(place_obj, key):
                setattr(place_obj, key, fields[key])
    place_obj.save()
    return jsonify(place_obj.to_dict()), 200

@app_views.route('/places_search', methods=['POST'])
def places_search():
    """
        places route to handle http method for request to search places
    """
    all_places = [p for p in storage.all('Place').values()]
    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')
    states = req_json.get('states')
    if states and len(states) > 0:
        all_cities = storage.all('City')
        state_cities = set([city.id for city in all_cities.values()
                            if city.state_id in states])
    else:
        state_cities = set()
    cities = req_json.get('cities')
    if cities and len(cities) > 0:
        cities = set([
            c_id for c_id in cities if storage.get('City', c_id)])
        state_cities = state_cities.union(cities)
    amenities = req_json.get('amenities')
    if len(state_cities) > 0:
        all_places = [p for p in all_places if p.city_id in state_cities]
    elif amenities is None or len(amenities) == 0:
        result = [place.to_json() for place in all_places]
        return jsonify(result)
    places_amenities = []
    if amenities and len(amenities) > 0:
        amenities = set([
            a_id for a_id in amenities if storage.get('Amenity', a_id)])
        for p in all_places:
            p_amenities = None
            if STORAGE_TYPE == 'db' and p.amenities:
                p_amenities = [a.id for a in p.amenities]
            elif len(p.amenities) > 0:
                p_amenities = p.amenities
            if p_amenities and all([a in p_amenities for a in amenities]):
                places_amenities.append(p)
    else:
        places_amenities = all_places
    result = [place.to_json() for place in places_amenities]
    return jsonify(result)
