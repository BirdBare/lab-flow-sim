import os
import pathlib
import sys

import django
import streamlit


def orm_setup():
    from django.conf import settings

    try:
        settings.DEBUG
        #Check if settings has been set. If it has then that means we do not need to run setup.
    
    except:
        sys.path.append(str(pathlib.Path(__file__).parent.parent.parent))

        if not streamlit.session_state.get("django_orm_setup", False):
            streamlit.session_state["django_orm_setup"] = True

            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_orm.django_config.settings")
            django.setup()
        # Only want to run once if not setup. Otherwise weird DB stuff can occur.
