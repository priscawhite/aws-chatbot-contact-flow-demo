# **Tech with Ease – Intelligent Contact Center Demo**

Welcome! This demo is of a small tech support contact center for a fictitious tech company called Tech with Ease. This company serves as the IT department for another company. Customers call or chat with the Tech with Ease support team to report IT-related issues and to get assistance.

This project demonstrates a full cloud-native contact center solution using:  
 - Amazon Connect
 - Amazon Lex
 - AWS Lambda
 - Amazon DynamoDB

This project also includes structured logging and test scenarios to simulate real-world production debugging using Amazon CloudWatch.

## **Design**
### **Contact Flow**
The Amazon Connect contact flow is designed to provide a streamlined, guided customer interaction from entry to resolution. It leverages Amazon Lex for natural language understanding, allowing users to interact using  voice or chat in a conversational way. The flow handles key actions such as capturing customer details, validating inputs, and routing requests dynamically based on intent. AWS Lambda functions are integrated for backend processing, including data persistence in DynamoDB and real-time validation. Error handling and fallback paths ensure a smooth user experience, while CloudWatch logging enables traceability and debugging. The overall design emphasizes modularity, making it easy to extend with additional intents or routing logic.

![Contact_flow](/img/flow_diagram.png)

### **Features**
 - AI-powered intent recognition
 - Automated ticket creation
 - Real-time ticket status lookup
 - Intelligent retry handling
 - Dynamic escalation to live agents
 - Attribute-based queue routing

 ## **Website & Serverless Chatbot**
 The web application is built as a lightweight, responsive frontend using HTML, CSS, and minimal JavaScript, with a focus on clean layout, usability, and fast performance. The chatbot interface is embedded via an iframe and styled to integrate seamlessly into the overall page design, with careful control over sizing, positioning, and responsiveness across devices. Static assets are hosted and delivered through Amazon S3 and Amazon CloudFront, enabling low-latency content delivery, caching, and improved global performance.

![Homepage_screenshot](/img/TechWithEase_chat_demo.gif)

## **Architecture**
This solution uses multiple AWS services integrated with Amazon Connect.

### **Core Services**
 - Amazon Connect – Contact center platform
 - Amazon Lex – Chatbot for chat and voice automation
 - AWS Lambda – Serverless logic
 - Amazon DynamoDB – Customer database
 - Amazon S3 – Storage for call recordings, logs, transcripts
 - Amazon CloudWatch – Metrics and alerts

### **High-Level Architecture**

![High-level architecture](/img/architecture_diagram.png)

### **Architecture Highlights**
 - Serverless backend
 - Event-driven processing
 - Context-aware agent handoff
 - Scalable and cost-efficient design

## **Customer Flows**
 - For customers that report a new issue for troubleshooting, the flow simulates new ticket creation and returns the confirmation with the ticket number to the customer.
 - Customers can request an update on the status of an existing ticket. The flow checks and returns the status to the customer. The customer is also offered an option to speak with an agent for additional assistance.
 - Customers with questions about billing are offered a link to the FAQ or the option to speak with an agent for additional assistance.
 - Fallback handling is in place where the customer's intent is not recognized. If intent recognition fails twice, the contact is escalated and queued to an agent.
 - Customers in queue are offered a callback option in the case that wait times are longer than usual.

## **Testing Strategy**
This project includes structured test scenarios and sample event payloads to simulate real-world interactions with the Lex bot and Lambda backend.

## **Repository Structure**
```
📂 main/
│── README.md
│── 📂 contact-flow/
│── 📂 dynamodb/
│── 📂 lex/
└── 📂 tests/
```
[**contact-flow**](/contact-flow/) ▸ Defines Amazon Connect contact flow architecture, including call routing logic and end-to-end customer interaction design   
[**dynamodb**](/dynamodb/)  ▸ Specifies DynamoDB schema design, configuration, and data access patterns supporting scalable session management  
[**lex**](/lex/)  ▸ Details Amazon Lex chatbot architecture, including intent modeling, slot management, and backend integrations  
[**tests**](/tests/)  ▸ Documents automated testing framework, covering end-to-end validation, scenario coverage, and system reliability checks

## **Future Updates**
Tech with Ease will continue to evolve to meet the needs of their customers! Check back later for new features!
| Feature 🌟 Wishlist |
|--------|
| Configure generative AI features (integration with Amazon Bedrock) for more natural, intelligent conversations with Lex |
| Integrate a Kendra index for the `BillingHelp` intent to enable users to ask questions about billing and get answers generated by an AI agent that sources an internal document repository |
| Configure a Kendra index for real-time agent assistance |
| Kinesis real-time data streams and intent analysis |
| CloudWatch dashboards and monitoring with SQS notifications |
| Agent workspace UI enhancements |
