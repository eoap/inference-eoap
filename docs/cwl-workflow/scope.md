When developers package and EO, they are in fact packaging their own software, written in a specific programming language, as a containerized application (or a set of containerized applications), to be described as an EO Application Package using the Common Workflow Language as described in the OGC proposed best practices.

To achieve this, developers follow the steps described below.

* Prepare one or more container images containing the execution dependencies of the software.
* Prepare the CWL CommandLineTool document(s) wrapping the command line tool available in container(s).
* **Prepare the CWL Workflow orchestrating CWL CommandLineTool document(s) wrapping the command line tool available container(s).**
* Test the application package in one or more execution scenarios.

This section shows how to do the step:

* Prepare the CWL Workflow orchestrating CWL CommandLineTool document(s) wrapping the command line tool available container(s).

### Orchestrating CWL CommandLineTools

The CWL `CommandLineTool`s wrapping the inference command-line tools had a single CWL class.

An Application Package must include at least one CWL `Workflow` class orchestrating the CWL `CommandLineTool` above.

We will need a CWL document with a list of process objects: a `Workflow` class and CWL `CommandLineTool` wrapping the Python command line tool. 

A `$graph` document does not have a process object at the root. Instead there is a `$graph` field which consists of a list of process objects.

Each process object must have an `id` field: 

```yaml
cwlVersion=1.0

$graph:
- class: Workflow
  id: main
  ...

- class: CommandLineTool
  id: inference
  ...
```

Workflow run fields cross-reference other processes in the document `$graph` using the `id` of the process object:

```yaml
cwlVersion=1.0

$graph:
- class: Workflow
  id: main
  steps:
    node_inference:
      run: "#inference"
      ...
  ...

- class: CommandLineTool
  id: inference
  ...
```

We propose the Workflow `tile-based-classification.cwl` reading a staged and converted to COG Sentinel-2 Level-1C acquisition orchestrating the inference Python command line tool.
