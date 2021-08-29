from .basket import Basket


def basket(request):
    """
        This function created for reaching the session from anywhere in our template.
    """
    return {
        "basket": Basket(request) 
    }
