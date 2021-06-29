# ************************************ ERROR MESSAGE FILE **********************************************#


def concat(error):
    """

    :param error:
    :return:
    """
    if isinstance(error, str):
        return ".".join(["backend.common", error])
    else:
        return "error message is not string type"


UR_PASS_AND_CONFRM_PASS_DONT_MATCH = concat("YourPassAndConfrmPassDontMatch")
PHONE_NUM_ALREADY_REGISTERED = concat("PhoneNumberAlreadRegistered")
THE_EMAIL_IS_ALREADY_REGISTERED = concat("TheEmailIsAlreadyRegistered")
EMAIL_REQUIRED = concat("Emailrequired")
UR_PASS_AND_CONFRM_PASS_DONT_MATCH = concat("YourPassAndConfrmPassDontMatch")
