# -*- coding: UTF-8 -*-

"""Runs Scala, PySpark and SQL statement through Spark using a REST endpoint in remote cluster.
Provides the %spark magic."""

# Copyright (c) 2015  aggftw@gmail.com
# Distributed under the terms of the Modified BSD License.

from __future__ import print_function
from IPython.core.magic import Magics, magics_class
from hdijupyterutils.ipythondisplay import IpythonDisplay

import sparkmagic.utils.configuration as conf
from sparkmagic.utils.sparklogger import SparkLog
from sparkmagic.utils.sparkevents import SparkEvents
from sparkmagic.utils.utils import get_session_info_html
from sparkmagic.utils.constants import MAGICS_LOGGER_NAME
from sparkmagic.livyclientlib.sparkcontroller import SparkController
from sparkmagic.livyclientlib.sqlquery import SQLQuery

@magics_class
class SparkMagicBase(Magics):
    def __init__(self, shell, data=None, spark_events=None):
        # You must call the parent constructor
        super(SparkMagicBase, self).__init__(shell)

        self.logger = SparkLog(u"SparkMagics")
        self.ipython_display = IpythonDisplay()
        self.spark_controller = SparkController(self.ipython_display)

        self.logger.debug("Initialized spark magics.")

        if spark_events is None:
            spark_events = SparkEvents()
        spark_events.emit_library_loaded_event()

    def execute_sqlquery(self, cell, samplemethod, maxrows, samplefraction,
                         session, output_var, quiet):
        sqlquery = self._sqlquery(cell, samplemethod, maxrows, samplefraction)
        df = self.spark_controller.run_sqlquery(sqlquery, session)
        if output_var is not None:
            self.shell.user_ns[output_var] = df
        if quiet:
            return None
        else:
            return df

    @staticmethod
    def _sqlquery(cell, samplemethod, maxrows, samplefraction):
        return SQLQuery(cell, samplemethod, maxrows, samplefraction)

    def _print_endpoint_info(self, info_sessions, current_session_id):
        if info_sessions:
            info_sessions = sorted(info_sessions, key=lambda s: s.id)
            html = get_session_info_html(info_sessions, current_session_id)
            self.ipython_display.html(html)
        else:
            self.ipython_display.html(u'No active sessions.')
