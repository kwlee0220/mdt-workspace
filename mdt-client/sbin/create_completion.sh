#!	/bin/bash

java -cp $MDT_CLIENT_HOME/mdt-client-all.jar picocli.AutoComplete mdt.cli.MDTCommandsMain -n mdt "$@"
