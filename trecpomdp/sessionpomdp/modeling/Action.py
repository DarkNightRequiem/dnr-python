
class UserAction:
    """
    User Domain-Level Actions
    """
    ADD_TERMS = 4
    REMOVE_TERMS = 5
    KEEP_TERMS = 6
    """
    User Communications-Level Actions
    """
    CLICKED_DOCUMENTS = 7


class EngineAction:
    """
    Engine Domain-Level Actions
    """
    INCREASE_WEIGHT = 8
    DECREASE_WEIGHT = 9
    KEEP_WEIGHT = 10

    """
    Engine Communications-Level Actions 
    """
    RETURNED_DOCUMENT = 11

