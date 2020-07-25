from kgb_afirm.base_bot import BaseBot


class FloriaBot(BaseBot):

    def __init__(self, owner_id: int, token: str, loop=None):
        """
        Create a new bot. Provide the owner id and optionally modify the description and sensitivity to text case.
        """

        bot_name = 'Floria'
        description = 'AFIRM: Affirmations For Immediately Recomposing Mindsets | by KGB'
        case_insensitive = True

        super().__init__(bot_name=bot_name, owner_id=owner_id, token=token, description=description,
                         case_insensitive=case_insensitive, loop=loop)
