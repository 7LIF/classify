################################################################################
##      Specifies the public interface of this module
################################################################################

__all__ = (
    'ViewModel',
)



################################################################################
##      Importing necessary modules
################################################################################

from typing import Any
import common.auth


################################################################################
##      ViewModel
################################################################################

class ViewModel(dict):
    def __init__(self, *args, **kargs):
        user = common.auth.get_current_user()
        user_id = user.user_id if user else None
        all = {
            'error': None,
            'error_msg': None,
            'user_id': user_id,
            'is_logged_in': user_id is not None,
        }
        all.update(kargs)
        super().__init__(*args, **all)

    def __getattr__(self, name: str) -> Any:
        return self[name]

    def __setattr__(self, name: str, value: Any) -> None:
        self[name] = value
