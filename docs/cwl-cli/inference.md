
### Goal 

Wrap the inference Python command line tool as a Common Workflow Language `CommandLineTool` and execute it with a CWL runner.

### Lab

This step has a dedicated lab available at `/workspace/inference-eoap/practice-labs/CommandLineTool.ipynb`

### How to wrap a step as a CWL CommandLineTool 

The CWL document below shows the inference Python command line tool step wrapped as a CWL CommandLineTool:

TODO 

```yaml linenums="1" hl_lines="9-12 49-53" title="cwl-cli/inference"
--8<--
cwl-cli/inference.cwl
--8<--
```

Let's break down the key components of this CWL document:

* `cwlVersion: v1.0`: Specifies the version of the CWL specification that this document follows.
* `class: CommandLineTool`: Indicates that this CWL document defines a command-line tool.
* `id: crop`: Provides a unique identifier for this tool, which can be used to reference it in workflows.
* `requirements`: Specifies the requirements and dependencies of the tool. In this case, it defines the following:
    * `InlineJavascriptRequirement`: This requirement allows the use of inline JavaScript expressions in the tool.
    * `EnvVarRequirement`: It sets environment variables. In this case, it sets the `PYTHONPATH` environment variable to "/app."
    * `ResourceRequirement`: Specifies resource requirements for running the tool, including the maximum number of CPU cores and maximum RAM.
    * `DockerRequirement`: This requirement specifies the Docker container to be used. It indicates that the tool should be executed in a Docker container with the image `localhost/crop:latest`.
* `baseCommand`: Defines the base command to be executed in the container. In this case, it's running a Python module called "app" with the command `python -m app`.
* `arguments`: This section is empty, meaning there are no additional command-line arguments specified here. The tool is expected to receive its arguments via the input parameters.
* `inputs`: Describes the input parameters for the tool, including their types and how they are bound to command-line arguments. The tool expects the following inputs:

TODO

    * `item`: A string representing the input STAC item (image) to be processed, bound to the `--input-item` argument.
    * `aoi`: A string representing the area of interest (AOI) as a bounding box, bound to the `--aoi` argument.
    * `epsg`: A string representing the EPSG code for the coordinate system, bound to the `--epsg` argument.
    * `band`: An array of strings representing the name of the bands to be extracted, bound to the `--band` argument.
* `outputs`: Specifies the tool's output. It defines an output parameter named `stac_catalog`, which is of type `Directory`. The outputBinding section specifies that the tool is expected to produce one or more files (glob: .) as output.

### Steps

Run the CWL document using the `cwltool` CWL runner to execute the tile based classification inference:


```console title="terminal"
--8<--
scripts/cwl-cli.sh
--8<--
```

### Expected outcome

The folder `/workspace/inference-eoap/runs` contains: 

```
(base) jovyan@jupyter-fbrito--training:~/inference-eoap$ tree runs
runs
TODO
2 directories, 4 files
```