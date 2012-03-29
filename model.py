# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the program FFM.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    model
#
# Purpose
#    Object model and scaffold for FFM
#
# Revision Dates
#    26-Mar-2012 (CT) Creation
#    ��revision-date�����
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _FFM                   import FFM
from   _GTW                   import GTW
from   _JNJ                   import JNJ
from   _MOM                   import MOM
from   _ReST                  import ReST
from   _TFL                   import TFL

from   _MOM.Product_Version   import Product_Version, IV_Number

import _FFM.import_FFM
import _GTW._OMP._Auth.import_Auth
import _GTW._OMP._PAP.import_PAP

import _GTW._Werkzeug.Scaffold

import _GTW._OMP._Auth.Nav
import _GTW._OMP._PAP.Nav
import _FFM.Nav

import _GTW._NAV.import_NAV
import _GTW._NAV.Console

import _GTW.HTML
import _ReST.To_Html

from   _TFL                     import sos
from   _TFL.I18N                import _, _T, _Tn
from   _TFL.Regexp              import Re_Replacer
from   _TFL._Meta.Once_Property import Once_Property
from   _TFL._Meta.Property      import Class_Property

import _TFL.CAO

import _GTW._AFS._MOM.Spec

GTW.AFS.MOM.Spec.setup_defaults ()

GTW.OMP.PAP.Phone.change_attribute_default         ("country_code", "43")

FFM.Version = Product_Version \
    ( productid           = u"FFM node data base"
    , productnick         = u"FFM"
    , productdesc         = u"Web application for FFM node data base"
    , date                = "26-Mar-2012 "
    , major               = 0
    , minor               = 1
    , patchlevel          = 0
    , author              = u"Christian Tanzer, Ralf Schlatterbeck"
    , copyright_start     = 2012
    , db_version          = IV_Number
        ( "db_version"
        , ("FFM", )
        , ("FFM", )
        , program_version = 1
        , comp_min        = 0
        , db_extension    = ".ffm"
        )
    )

class Scaffold (GTW.Werkzeug.Scaffold) :

    ANS                   = FFM
    cmd__base__opts_x     = \
        ( "-config:C=~/.ffm.config?File specifying defaults for options"
        , "-home_url_root:S=http://ffm.funkfeuer.at"
        )
    cmd__copyright_start  = 2012 ### XXX ???

    default_db_name       = bytes ("test")
    nick                  = u"FFM"
    PNS_Aliases           = dict \
        ( Auth            = GTW.OMP.Auth
        , PAP             = GTW.OMP.PAP
        )
    SALT                  = bytes \
        ( "to be done ")

    @classmethod
    def create_nav (cls, cmd, app_type, db_url, ** kw) :
        import nav
        result = nav.create (cmd, app_type, db_url, ** kw)
        result.add_entries \
            ( [ dict
                  ( sub_dir         = "Admin"
                  , short_title     = "Admin"
                  , pid             = "Admin"
                  , title           = _ ("Administration of FFM node database")
                  , head_line       = _ ("Administration of FFM node database")
                  , login_required  = True
                  , Type            = GTW.NAV.E_Type.Site_Admin
                  , entries         =
                      [ cls.nav_admin_group
                          ( "FFM"
                          , _ ("Administration of node database")
                          , "FFM"
                          , permission = GTW.NAV.In_Group ("FFM-admin")
                          )
                      , cls.nav_admin_group
                          ( "PAP"
                          , _ ("Administration of persons/addresses...")
                          , "GTW.OMP.PAP"
                          , permission = GTW.NAV.In_Group ("FFM-admin")
                          )
                      , cls.nav_admin_group
                          ( _ ("Users")
                          , _ ("Administration of user accounts and groups")
                          , "GTW.OMP.Auth"
                          , permission = GTW.NAV.Is_Superuser ()
                          )
                      ]
                  )
              , dict
                  ( src_dir         = _ ("Auth")
                  , pid             = "Auth"
                  , prefix          = "Auth"
                  , short_title     = _ (u"Authorization and Account handling")
                  , Type            = GTW.NAV.Auth
                  , hidden          = True
                  )
              , dict
                  ( src_dir         = _ ("L10N")
                  , prefix          = "L10N"
                  , short_title     =
                    _ (u"Choice of language used for localization")
                  , Type            = GTW.NAV.L10N
                  , country_map     = dict \
                      ( de          = "AT")
                  )
              , dict
                  ( name            = "STOP"
                  , delay           = 2
                  , Type            = GTW.NAV.Stopper
                  , hidden          = True
                  )
              , dict
                  ( Type            = GTW.NAV.Robot_Excluder
                  )
              ]
            )
        if cmd.debug :
            result.add_entries \
                ( [ dict
                      ( src_dir         = _ ("Console")
                      , name            = "Console"
                      , short_title     = _(u"Console")
                      , title           = _(u"Interactive Python interpreter")
                      , Type            = GTW.NAV.Console
                      , permission      = GTW.NAV.Is_Superuser ()
                      )
                  ]
                )
        if result.DEBUG :
            scope = result.__dict__.get ("scope", "*not yet created*")
            print ("NAV created, Scope", scope)
        return result
    # end def create_nav

    @classmethod
    def fixtures (cls, scope) :
        import fixtures
        return fixtures.create (scope)
    # end def fixtures

    @Class_Property
    @Once_Property
    def jnj_src (cls) :
        import nav
        return nav.jnj_src
    # end def jnj_src

    @Class_Property
    @Once_Property
    def web_src_root (cls) :
        import nav
        return nav.web_src_root
    # end def web_src_root

# end class Scaffold

opts = tuple \
    ( Scaffold.cmd__base__opts
    + Scaffold.cmd__run_server__opts
    )

def scope (cmd = None) :
    args = (cmd.db_url, cmd.db_name, cmd.create) if cmd else ()
    return Scaffold.scope (* args)
# end def scope

_Command = Scaffold.cmd

if __name__ == "__main__" :
    _Command ()
### __END__ model