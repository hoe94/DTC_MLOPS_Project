def Credit_Mix_dict_mapping(key, value):
    """Encode the categorical value from request value corresponding to dictionary
    return the mapped dictionary
    """
    Credit_Mix_dict = {"Standard": 1, "Good": 2, "_": 3, "Bad": 4}
    columns_dict = {}

    if (
        value not in Credit_Mix_dict.keys()
    ):  # if the value doesnt exist in dictionary key
        columns_dict[key] = 0  # map the categorical value into 0
        return columns_dict
    else:
        dict_value = Credit_Mix_dict[value]  # map the categorical value
        columns_dict[key] = dict_value
        return columns_dict


def Occupation_dict_mapping(key, value):
    """Encode the categorical value from request value corresponding to dictionary
    return the mapped dictionary
    """
    Occupation_dict = {
        "Lawyer": 1,
        "Architect": 2,
        "Engineer": 3,
        "Scientist": 4,
        "Mechanic": 5,
        "Others": 0,
    }
    columns_dict = {}

    if (
        value not in Occupation_dict.keys()
    ):  # if the value doesnt exist in dictionary key
        columns_dict[key] = 0  # map the categorical value into 0
        return columns_dict
    else:
        dict_value = Occupation_dict[value]  # map the categorical value
        columns_dict[key] = dict_value
        return columns_dict


def Payment_Behaviour_dict_mapping(key, value):
    """Encode the categorical value from request value corresponding to dictionary
    return the mapped dictionary
    """
    Payment_Behaviour_dict = {
        "Low_spent_Small_value_payments": 1,
        "High_spent_Medium_value_payments": 2,
        "Low_spent_Medium_value_payments": 3,
        "High_spent_Large_value_payments": 4,
        "High_spent_Small_value_payments": 5,
        "Low_spent_Large_value_payments": 6,
    }
    columns_dict = {}

    if (
        value not in Payment_Behaviour_dict.keys()
    ):  # if the value doesnt exist in dictionary key
        columns_dict[key] = 0  # map the categorical value into 0
        return columns_dict
    else:
        dict_value = Payment_Behaviour_dict[value]  # map the categorical value
        columns_dict[key] = dict_value
        return columns_dict


def Payment_of_Min_Amount_dict_mapping(key, value):
    """Encode the categorical value from request value corresponding to dictionary
    return the mapped dictionary
    """
    Payment_of_Min_Amount_dict = {"Yes": 1, "No": 2, "NM": 3}
    columns_dict = {}

    if (
        value not in Payment_of_Min_Amount_dict.keys()
    ):  # if the value doesnt exist in dictionary key
        columns_dict[key] = 0  # map the categorical value into 0
        return columns_dict
    else:
        dict_value = Payment_of_Min_Amount_dict[value]  # map the categorical value
        columns_dict[key] = dict_value
        return columns_dict
