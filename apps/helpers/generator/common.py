# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from django.conf import settings

#from decouple import config

# ENV 
#GH_TOKEN    = config('GH_TOKEN'   , None)
#GH_ACCOUNT  = config('GH_ACCOUNT' , None)

#GH_TOKEN2   = config('GH_TOKEN2'  , None)
#GH_ACCOUNT2 = config('GH_ACCOUNT2', None)

#GH_TOKEN3   = config('GH_TOKEN3'  , None)
#GH_ACCOUNT3 = config('GH_ACCOUNT3', None)

#GH_CREDENTIALS = {}

#GH_CREDENTIALS[ GH_ACCOUNT  ] = GH_TOKEN
#GH_CREDENTIALS[ GH_ACCOUNT2 ] = GH_TOKEN2
#GH_CREDENTIALS[ GH_ACCOUNT3 ] = GH_TOKEN3

# Globals 
DIR_ROOT          = settings.BASE_DIR
DIR_TMPL          = os.path.join( DIR_ROOT, 'templates', 'generator' )
DIR_GEN_APPS      = os.path.join( DIR_ROOT, 'generated_code' )

INPUT_JSON        = os.path.join( DIR_ROOT, 'sources', 'input-template.json'      )
INPUT_JSON_VOLT   = os.path.join( DIR_ROOT, 'sources', 'input-template-volt.json' )

DIR_DJ_CORE       = 'core'
DIR_DJ_HOME       = 'home'

FILE_DJ_MANAGE_s   = 'manage.py'
FILE_DJ_ENV_s      = '.env'
FILE_DJ_DEPS_s     = 'requirements.txt'
FILE_DJ_URLS_s     = os.path.join( DIR_DJ_CORE , 'urls.py'          )
FILE_DJ_SETTINGS_s = os.path.join( DIR_DJ_CORE , 'settings.py'      )
FILE_DJ_MODELS_s   = os.path.join( DIR_DJ_HOME , 'models.py'        )

FILE_CI_BUILD_s    = 'build.sh'
FILE_DOCKER_s      = 'Dockerfile'


class COMMON:

    NULL              = None # not set
    NA                = -1   # not set
    OK                =  0   # All good   (unix style)
    ERR               =  1   # Err bumped (unix style)
    NOT_FOUND         =  2   # file or directory not found
    INPUT_ERR         =  3   # file or directory not found

    POS_FIRST         = 'FIRST'
    POS_END           = 'END'
    
    # Settings vars typologies 
    CFG_VAR_NA        = 10 # Type is undetected
    CFG_VAR_SIMPLE    = 11 # Ex: SECRET_KEY
    CFG_VAR_LIST      = 12 # Ex: INSTALLED_APPS, MIDDLEWARE
    CFG_VAR_DICT      = 13 # List of Dicts, Ex: AUTH_PASSWORD_VALIDATORS 

    TAB               = '    '
    TAB2              = TAB  + TAB
    TAB3              = TAB2 + TAB

    TYPE_STRING       = 'string'
    TYPE_STRING_DJ    = 'models.CharField'

    TYPE_TEXT         = 'text'
    TYPE_TEXT_DJ      = 'models.TextField'

    TYPE_INT          = 'number'
    TYPE_INT_DJ       = 'models.IntegerField'    

# Recover errors for COMMON class
def errInfo( aErrorCode ):

    if COMMON.NA         == aErrorCode: return 'Not Set'
    if COMMON.ERR        == aErrorCode: return 'Error Generic'
    if COMMON.OK         == aErrorCode: return 'OK'
    if COMMON.NOT_FOUND  == aErrorCode: return 'Not Found'
    if COMMON.INPUT_ERR  == aErrorCode: return 'Input error'

    return str( aErrorCode )

def commonTxt( aCode ):

    if COMMON.CFG_VAR_NA     == aCode: return 'CFG Var unknown typology'
    if COMMON.CFG_VAR_SIMPLE == aCode: return 'CFG Var SIMPLE'
    if COMMON.CFG_VAR_LIST   == aCode: return 'CFG Var LIST'
    if COMMON.CFG_VAR_MIXED  == aCode: return 'CFG Var MIXT (list of dicts)'

    return str( aErrorCode )
 
