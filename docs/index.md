# Introduction 

Platforms for the exploitation of Earth Observation (EO) data have been developed by public and private companies in order to foster the usage of EO data and expand the market of Earth Observation-derived information. A fundamental principle of the platform operations concept is to move the EO data processing service’s user to the data and tools, as opposed to downloading, replicating, and exploiting data ‘at home’. In this scope, previous OGC activities initiated the development of an architecture to allow the ad-hoc deployment and execution of applications close to the physical location of the source data with the goal to minimize data transfer between data repositories and application processes.

The OGC published the _Best Practice for Earth Observation Application Package_, a document defining the Best Practice to package and deploy Earth Observation Applications in an Exploitation Platform. The document is targeting the implementation, packaging and deployment of EO Applications in support of collaborative work processes between developers and platform owners.

The Best Practice includes recommendations for the application design patterns, package encoding, container and data interfaces for data stage-in and stage-out strategies focusing on three main viewpoints: Application, Package and Platform.

The focus of this documentation set is the inference using an ONNX model. 

## The model 

The model is a Convolutional Neural Network (CNN) trained with Keras against the benchmark dataset EuroSAT. 

