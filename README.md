# iva-bedside

*iva-bedside (intelligent virtual assistant)* is a response to chronic and severe staffing issues in the nursing industry.

A patient is 7% more likely to die for every additional patient their nurse has to care for. *(The Lancet, 2014)*

IVA allows nurses to focus on the most important tasks at hand so they can deliver the best care possible.

## Abstract
IVA is a multilingual, voice-controlled AI assistant for clinical inpatient settings. IVA utilizes patient medical charts to assist accurately and in context per case. Additionally, IVA can recognize and initiate commands from natural language.

## Usage
IVA provides low-level support for patients, covering a wide range of tasks that can be safely automated. Tasks that cannot be automated safely are recognized and passed safely through IVA as requests to human clinical staff.

## Limitations
There are many nuances to human conversation that cannot be replicated with the same accuracy with a voice assistant. IVA does not provide the same level or type of support as humans, and therefore does not replace human clinical staff.

## Utilities
Leverages OpenAI's GPT-3 for natural language and Microsoft Azure for STT + TTS

## Examples

>**Patient:** "I need help getting out of bed."  
>**IVA:** "Hi. I'll call someone to help you get out of bed right away. **\[FALL RISK REQUEST\]**"

>**Patient:** "I'm hungry."  
>**IVA:** "Ok. I'll have someone bring you a menu. **\[MEAL REQUEST\]**"