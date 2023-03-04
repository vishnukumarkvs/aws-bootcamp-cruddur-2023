# Week 2 — Distributed Tracing

# Basics
## Observability
- Observability provides deep visibility into modern distributed applications for faster, automated problem identification and resolution.
- In observability, a span and a tracer are both important concepts in distributed tracing, but they have different roles.
- A span is a unit of work or activity within a system that is being traced or monitored. It represents a single operation or event that occurs as part of a distributed system transaction, such as a database query, a network request, or a function call. Each span contains information about the start and end time of the activity, as well as metadata about the activity.
- A tracer, on the other hand, is an object that is responsible for managing and coordinating the collection of spans. A tracer is typically instantiated at the beginning of a transaction and is used to create and manage spans as the transaction progresses.

## Open Telemetry (OTEL)
- OpenTelemetry is a set of tools, APIs, and SDKs that are used to collect, manage, and export observability data (metrics, traces, and logs) from cloud-native software applications. It is open-source managed by CNCF
- Honeycomb, AWS Xray uses OpenTelemetry in its backend.

### M.E.L.T - application emits signals called MELT
- Metrics
  - These are measurements collected at regular intervals must have a timestamp and name, one or more numeric values

- Event
  - Events are discrete occurrences within an application that can be logged and analyzed. 
  - Events can include user actions, system events, and error messages, among other things

- Logs
  - Come directly from app
  - System.out.print() or console.log()

- Traces
  - Traces follow a request or path from the initial request to the returned output
  - records casual chain of events

## Honeycomb
- Honeycomb is a cloud-based observability platform that allows developers to quickly and easily understand the behavior and performance of their software applications.
- Instrumenting our application:-
    - Adding code to our app so that it can collect and send telemetry data


## AWS XRAY
- AWS Service used for Observability
- aws_xray_sdk = SDK used fotr instrumention python application
- It has segments, subsegments

# Hard Assignments
- Completed all tasks

## Difficulties faced
- AWS Xray creating segments and subsegments. Able to make it work by passing xray_recorder as object(Idea: Olleys article). But still getting SegmentationNotFound in some cases.
- CloudWatch and AWS Xray not working together. If we initialise Xray before Cloudwatch, the workaround above doesnt work anymore
- If xray initialised after cloudwatch, xray is overriding the logging functionality of cloudwatch
- So, I disabled xray for cloudwatch demo. Will try to fix this in coming weeks 

## External Links that helped me
- https://pypi.org/project/aws-xray-sdk/
- https://pypi.org/project/watchtower/
- https://olley.hashnode.dev/aws-free-cloud-bootcamp-instrumenting-aws-x-ray-subsegments

