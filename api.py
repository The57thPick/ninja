import hug

from data.models import Ninja


@hug.get(examples='first_name=Brent&last_name=Steffensen')
def rating(first_name: hug.types.text, last_name: hug.types.text):
    """Returns the given competitor's Ninja Rating.
    """
    return {'speed': '', 'consistency': '', 'success': ''}
