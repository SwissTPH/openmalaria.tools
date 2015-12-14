# openmalaria.tools
This is a set of (command line) tools for end users for usage in combination with the [openMalaria](https://github.com/SwissTPH/openmalaria) simulator program from [SwissTPH](https://github.com/SwissTPH).

No programming experience is required to use these tools.

It contains scripts for
* Plotting openmalaria results with _[plotResults.py](openmalaria/tools/plotResult.py)_
* Generating Schema Documentation from a provided **[schema.xsd](https://github.com/SwissTPH/openmalaria/tree/develop/schema)** with _[generateDoc.py](openmalaria/tools/generateDoc.py)_
* Read Output files  with _[readOutput.py](openmalaria/tools/readOutput.py)_ (this is used by `plotResults.py`)
* Reformat XML files with _[reformat_xmls.py](openmalaria/tools/reformat_xmls.py)_
* translate XML files with _[translateXML.py](openmalaria/tools/translateXML.py)_

Reasons to implement openmalaria.tools as a separate project from vecnet.openmalaria

1. Different license can be used (say user tools can be GPL, while core library can use less restrictive license)
1. openmalaria.tools will have a lot of dependencies on other libraries (lxml, mathlibplot and so on).  vecnet.openmalaria should have as few dependencies as possible - ideally, none.
1. openmalaria.tools is focused on end users, and do not require any programming to be used. vecnet.openmalaria is a library and is intended to be used by python programmers.
1. We may have different versioning approaches for vecnet.openmalaria and openmalaria.tools. For example, the tools may have a version number that tracks the newest OM schema version it supports (e.g., OM Toolkit v33.# supports OM versions up to and including version 33).  In contrast, the vecnet.openmalaria library should use semantic versioning, and only change its major version when there's a backward-incompatible change to its API.

## Tool documentation

Some documentation can be found [in the openmalaria wiki](https://github.com/SwissTPH/openmalaria/wiki/UtilsRunScripts).

### Result plotting

The `plotResults.py` script is a tool to quickly plot standard outputs (not the "continuous" outputs) from one or a small number of simulations. [Documentation can be found here.](https://github.com/SwissTPH/openmalaria/wiki/UtilsRunScripts#plotresultpy)

### Generating documentation

This tool generates a set of wiki pages from XML Schema Documents (XSD). [Here is the output for OpenMalaria schemas.](https://github.com/SwissTPH/openmalaria/wiki/GeneratedSchemaDocIndex)

Usage:

1.  Change to the directory where you want the output
2.  Run, giving the path to all schemas of interest (e.g. `/path/to/generateDoc.py /path/to/schemas/schema_*.xsd`)

Note that the tool supports only the limited schema features found in OpenMalaria schemas and will likely need extension for any other schema.

### XML tools

The script `reformat_xmls.py` standardises indentation, new-lines and general usage of white-space in an XML file. It is an alternative to `xmllint --format`. Usage: `./reformat_xmls.py -p folder_path | file_path`

Another script, `translateXML.py`, eases migration of existing OpenMalaria scenarios (XML files) to later versions of OpenMalaria. Usage is simply `translateXML.py -t 33 scenario.xml`. Full instructions below:

    usage: translateXML.py [-h] [-t VER] [-d DIR | -i | --db DBNAME] [-u USER]
                        [-r RUN_ID] [--mol5d-pairwise] [--add-human-weight]
                        [FILE [FILE ...]]

    This tool translates one or more OpenMalaria scenario files (XML) from one
    version to the next.

    positional arguments:
    FILE                  A file to translate. Multiple files may be specified.

    optional arguments:
    -h, --help            show this help message and exit
    -t VER, --target-version VER
                            Target version for translation. Default: 33
    -d DIR, --dest DIR    Destination directory for translated scenarios
    -i, --in-place        If set, files will be updated in-place (incompatible
                            with -d option)
    --db DBNAME           If set, files will be updated from the scenarios table
                            of this database.
    -u USER, --user USER  Username to connect to database with. If not set, will
                            try to connect without username.
    -r RUN_ID, --run-id RUN_ID
                            [DB mode] If given, only scenarios with this run_id                                               
                            are updated; if not, all are updated.                                                             
    --mol5d-pairwise      Update XMLs using a 5-day time step to use the                                                    
                            Molineaux model with pairwise sampling.                                                           
    --add-human-weight    Add scenario/model/human/weight data to scenarios                                                 
