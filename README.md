# simple-flow

The **simple-flow** library provides basic building blocks for creating and 
executing simple workflows. It not only contains abstract superclasses that can 
be used to implement new actors (= operators), but also a set of useful actors 
for controlling the flow of data and simple I/O.

Inspired by the [ADAMS](https://adams.cms.waikato.ac.nz/) workflow system, 
there are no explicit connections between the actors. Instead, the nesting
and use of *control actors* determines how the data flows and how the flow is
being executed. The actors themselves can be *input consumers* and/or
*output producers*. Data itself is wrapped in a *Token* wrapper.
Multiple outputs a managed by outputting *container* objects, from which 
individual values can be retrieved with the *ContainerValuePicker* control actor.
Objects can be parked and retrieved from *internal storage* using special actors,
allowing the use of the same object in multiple locations.


## Actors

### Control actors

Control actors *control* either the flow of data or the execution of the flow: 

* `simflow.control.Flow` - the outermost actor that manages a complete workflow
* `simflow.control.Branch` - forwards the same input to all its branches and executes them one after the other 
* `simflow.control.ContainerValuePicker` - obtains an object from a special `Container` object via its name 
* `simflow.control.Sequence` - combines multiple operators into a sequence of steps; only takes input, does not generate output 
* `simflow.control.Stop` - stops the flow execution when reached 
* `simflow.control.Tee` - forks off the incoming data to a sub-flow before forwarding the data 
* `simflow.control.Trigger` - executes the specified sub-flow whenever an input token arrives, but does not forward the input to the sub-flow  

### Sources

Source actors only generate data:

* `simflow.source.CombineStorage` - expands the storage item expression and forwards the generated string 
* `simflow.source.FileSupplier` - forwards the specified files one by one 
* `simflow.source.ForLoop` - outputs the value of loop variable  
* `simflow.source.GetStorageValue` - outputs the named object from the internal storage 
* `simflow.source.ListFiles` - lists the files/dirs in the specified directory 
* `simflow.source.Start` - forwards a dummy token to trigger actor execution 
* `simflow.source.StringConstants` - outputs the specified strings one by one 

### Transformers

Transformers receive input data and generate output from it:

* `simflow.transformer.Convert` - applies the specified conversion object to the incoming data and forwards the generated output 
* `simflow.transformer.DeleteFile` - deletes the incoming files (if they match the regexp) 
* `simflow.transformer.DeleteStorageValue` - deletes the specified object from the internal storage 
* `simflow.transformer.InitStorageValue` - initializes the specified storage value with an initial value  
* `simflow.transformer.MathExpression` - evaluates a mathematical expression using the input value in its expression
* `simflow.transformer.PassThrough` - dummy actor that just forwards the input data 
* `simflow.transformer.SetStorageValue` - stores the incoming data in internal storage under the specified name 
* `simflow.transformer.UpdateStorageValue` - updates the specified internal storage item using the provided expression 

### Sinks

Sinks only receive data:

* `simflow.sink.Console` - simply outputs the incoming data on stdout 
* `simflow.sink.DumpFile` - stores the string representation of the incoming data in a file (can be appended) 
* `simflow.sink.Null` - consumes the incoming data without doing anything 


## Examples

* [output_actor_help.py](examples/output_actor_help.py) - generates and outputs help for an actor
* [for_loop.py](examples/for_loop.py) - how to use the `ForLoop` actor 
* [init_storage_value.py](examples/init_storage_value.py) - how to use the `InitStorageValue` actor 
* [list_files.py](examples/list_files.py) - lists files in the temp directory 
* [math_expression.py](examples/math_expression.py) - applies a mathematical expression to the input data
* [stop_flow.py](examples/stop_flow.py) - stops the execution when a certain condition is satisfied 
* [update_storage_value.py](examples/update_storage_value.py) - updates an object in storage using a mathematical expression 
