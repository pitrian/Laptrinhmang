# Lab 1.6 – AI-enhanced Debugging

## Objective
Use AI tools to identify bugs and optimize an asynchronous network application.

## Buggy Code Analysis
The initial async server contained multiple issues:
- Missing await for asynchronous read operation
- Missing drain after write
- Connection not properly closed

These issues caused unstable behavior under load.

## AI-assisted Debugging
An AI model was used to analyze the buggy code.
The AI successfully identified missing await statements and resource management issues.

## Fixed Implementation
After applying AI suggestions:
- All async operations are properly awaited
- Connections are gracefully closed
- Exception handling is added

## Conclusion
AI-assisted debugging helps quickly identify subtle issues in asynchronous network programming and improves code reliability and performance.
