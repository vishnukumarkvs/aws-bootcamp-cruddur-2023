# Week 2 — Distributed Tracing

1. [Basics](#basics)
2. [Difficulties faced](#difficulties-faced)

[Work](#work)
1. [Honeycomb](#honeycomb)
2. [AWS XRay](#aws-xray)
3. [AWS XRay Traces and Segments](#aws-xray-traces-and-segments)
4. [Cloudwatch](#cloudwatch)
5. [Rollbar](#rollbar)

## Basics
### Observability
- Observability provides deep visibility into modern distributed applications for faster, automated problem identification and resolution.
- In observability, a span and a tracer are both important concepts in distributed tracing, but they have different roles.
- A span is a unit of work or activity within a system that is being traced or monitored. It represents a single operation or event that occurs as part of a distributed system transaction, such as a database query, a network request, or a function call. Each span contains information about the start and end time of the activity, as well as metadata about the activity.
- A tracer, on the other hand, is an object that is responsible for managing and coordinating the collection of spans. A tracer is typically instantiated at the beginning of a transaction and is used to create and manage spans as the transaction progresses.

### Open Telemetry (OTEL)
- OpenTelemetry is a set of tools, APIs, and SDKs that are used to collect, manage, and export observability data (metrics, traces, and logs) from cloud-native software applications. It is open-source managed by CNCF
- Honeycomb, AWS Xray uses OpenTelemetry in its backend.

### M.E.L.T
- Application emits signals called MELT
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


# Difficulties faced
- AWS Xray creating segments and subsegments. Able to make it work by passing xray_recorder as object(Idea: Olleys article). But still getting SegmentationNotFound in some cases.
- CloudWatch and AWS Xray not working together. If we initialise Xray before Cloudwatch, the workaround above doesnt work anymore
- If xray initialised after cloudwatch, xray is overriding the logging functionality of cloudwatch
- So, I disabled xray for cloudwatch demo. Will try to fix this in coming weeks 

## External Links that helped me
- https://pypi.org/project/aws-xray-sdk/
- https://pypi.org/project/watchtower/
- https://olley.hashnode.dev/aws-free-cloud-bootcamp-instrumenting-aws-x-ray-subsegments

# Work
### Honeycomb
- Created Trace and Span, also added custom attributes to span
![custom attributes](https://user-images.githubusercontent.com/116954249/222916857-c2308c62-bf9f-431e-add2-dfe6c0d9acef.png)

- Overall Chart and heatmap
<table>
  <tr>
    <td><img src="https://user-images.githubusercontent.com/116954249/222916952-9d239c21-0a56-4c4c-94a8-6b0ead8f06f7.png" alt="Overall Chart"></td>
    <td><img src="https://user-images.githubusercontent.com/116954249/222916962-73f628c0-fbd9-4d53-bf18-11e25c5998dd.png" alt="Heatmap"></td>
  </tr>
</table>

### AWS XRay
- Created Sampling Rule and Xray Group
<table>
  <tr>
    <td><img src="https://user-images.githubusercontent.com/116954249/222917076-c41f17c7-49e9-4f08-bea4-4b004a3b3320.png" alt="Sampling Rule"></td>
    <td><img src="https://user-images.githubusercontent.com/116954249/222917089-358e8f85-7b8b-4924-8122-c7042361f8aa.png" alt="XRay Group"></td>
  </tr>
</table>
 
- Xray logs 

![xray-logs](https://user-images.githubusercontent.com/116954249/222917177-e2863f55-cd45-4162-bcb2-42f01b6a7f87.png)

### AWS XRay Traces and Segments
- For Notification Activities Service - Segemnt timeline

![tracenotification](https://user-images.githubusercontent.com/116954249/222917349-66619203-9cba-4eb2-ac09-580379847d87.png)

- Metadata for segment

![notificationmetadata](https://user-images.githubusercontent.com/116954249/222917342-4c8e3043-f8e8-475e-8009-3ffee2662fa4.png)

### Cloudwatch
- Configured Clouwatch logger in app
- Disabled Xray with `AWS_XRAY_SDK_ENABLED: "False"`. Xray and Cloudwatch not working simultaneiusly
- Traces

![cloudwatch-traces](https://user-images.githubusercontent.com/116954249/222917619-3452a0c7-b1aa-4d5b-af6f-a500c20f0926.png)

### Rollbar
- Configured Rollbar

![rollbar1](https://user-images.githubusercontent.com/116954249/222917641-52223d7d-5213-49de-9789-de31ec5c9dc7.png)

