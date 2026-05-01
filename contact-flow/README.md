# **Tech with Ease Contact Flows**

## **Overview**
These flows manage the end-to-end customer experience, ranging from initial welcome interactions to sophisticated queue routing and automated callback handling.

---

## **Main Flow**
This is the primary entry point for all incoming customer contacts.

### Key Features & Workflow:
**Initialization**  
Upon entry, the flow sets core contact attributes (`retryCount` = 0, `isEscalated` = false) to ensure a clean tracking state.  
**Automated Interaction**  
Utilizes the `TechWithEaseSupportBot` (Amazon Lex V2) to greet the customer and determine the nature of their request.  
**Intelligent Routing**
* **Billing Support:** Specifically routes callers to the Billing queue based on Lex intent matching ("billing").
    * **Tech Support Tier 1:** Routes general tech inquiries.
    * **Tech Support Tier 2:** Acts as a fallback for escalated issues or instances where the caller reaches retry limits.
* **Escalation Handling:** Contains logic to check the `escalateToAgent` attribute, allowing the system to pivot the conversation if the bot cannot resolve the issue.  

**Event Hook Integration**  
Registers the `TechWithEase_CallbackFlow` as an event hook, enabling callback capabilities while the customer is in the queue.

![MainFlow](/contact-flow/TechWithEase_MainFlow.png)

---

## **Callback Flow**
This flow is triggered when a customer chooses to receive a callback instead of waiting in the queue.

### Key Features & Workflow:
**Queue Experience**  
Uses `MessageParticipantIteratively` to play "CustomerQueue.wav" while remaining interruptible.  
**Callback Offer**  
Engages the Lex V2 Bot to confirm if the user prefers a callback.  
**Data Collection & Validation**
* Captures the user's phone number.
* Validates the number using the `UpdateContactCallbackNumber` node to ensure the contact can be reached.  

**Callback Scheduling**  
* **Mode:** `AgentFirst` (The system attempts to reach an agent before initiating the call to the customer).
* **Initial Delay:** 90 seconds
* **Retry Delay:** 600 seconds
* **Max Attempts:** 1

**Closure**  
Confirms the callback request to the customer and disconnects the caller.

![CallbackFlow](/contact-flow/TechWithEase_CallbackFlow.png)
