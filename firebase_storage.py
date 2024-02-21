import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("./firebase-admin-sdk.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://fota-2f692-default-rtdb.europe-west1.firebasedatabase.app/'
})


def get_db():
    """
    A function that returns the database object.
    """
    return db


def get_ref():
    """
    This function returns a reference to the root of the database.
    """
    return db.reference('/')


def get_ref_child(child):
    """
    Get a reference to the specified child node in the database.

    Parameters:
    child (str): The name of the child node.

    Returns:
    Reference: A reference to the specified child node in the database.
    """
    return db.reference(child)


def get_item(ref, item):
    """
    Retrieves an item from the reference based on the specified item parameter.

    :param ref: The reference to the data structure.
    :param item: The item to retrieve from the reference.
    :return: The retrieved item from the reference.
    """
    return ref.child(item).get()


def get_item_by_name(name):
    """
    Retrieves an item by its name from the 'Programmes' collection.

    Args:
        name (str): The name of the item to retrieve.

    Returns:
        dict or None: The item with the matching name if found, otherwise None.
    """
    try:
        if name is None:
            return None
        ref = get_ref()
        programmes = ref.child("Programmes").get()
        if programmes is None:
            return None
        for programme_key, programme_value in programmes.items():
            if programme_value.get("name") == name:
                return programme_value
        return None
    except Exception as e:
        print(f"Error retrieving item with name '{name}': {e}")
        return None

