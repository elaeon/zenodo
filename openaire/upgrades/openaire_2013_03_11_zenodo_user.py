# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2013 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

import warnings
from invenio.dbquery import run_sql
from invenio.textutils import wait_for_user


depends_on = ['openaire_2013_03_07_zenodo_collections']


def info():
    return "Migration of Orphan users"


def do_upgrade():
    """ Implement your upgrades here  """
    from invenio.openaire_deposit_config import CFG_OPENAIRE_DEPOSIT_PATH
    import shutil
    import os

    # Remove all but the admin user
    res = run_sql("SELECT id FROM user WHERE email='lars.holm.nielsen@cern.ch'")

    run_sql("DELETE FROM user WHERE id!=%s", res[0])
    run_sql("DELETE FROM user_accROLE WHERE id_user!=%s", res[0])
    run_sql("DELETE FROM user_bskBASKET")
    run_sql("DELETE FROM user_msgMESSAGE")
    run_sql("DELETE FROM user_query")
    run_sql("DELETE FROM user_usergroup")

    # Set all auto-complete authorships and keywords to the admin user
    run_sql("UPDATE IGNORE OpenAIREauthorships SET uid=176, publicationid=''")
    run_sql("UPDATE IGNORE OpenAIREkeywords SET uid=176, publicationid=''")

    # Remove all depositions from old users
    run_sql("DELETE FROM eupublication")

    # Remove previous depositions
    shutil.rmtree(CFG_OPENAIRE_DEPOSIT_PATH)
    os.makedirs(CFG_OPENAIRE_DEPOSIT_PATH)


def estimate():
    """  Estimate running time of upgrade in seconds (optional). """
    return 5


def pre_upgrade():
    """  Run pre-upgrade checks (optional). """
    try:
        from invenio.openaire_deposit_config import CFG_OPENAIRE_DEPOSIT_PATH
        import shutil
    except ImportError:
        raise RuntimeError("This does not seem to be an OpenAIRE installation. Cannot import 'openaire_deposit_config'.")


def post_upgrade():
    """  Run post-upgrade checks (optional). """
    # Example of issuing warnings:
    # warnings.warn("A continuable error occurred")
