

## Issue

The model is deployed on the TRIPTON server; however, a bug is causing the server to crash when attempting to load the model onto the actual graphics card. The model is over 50GB in size, and identifying the cause of the bug is time-consuming, resulting in constraints for the current hands-on exercises. We apologize for any inconvenience this may cause.

so the example3 practice has been replaced with example 2-2. 

thanks

##  the rapid performance improvements in open-source LLM

![image](https://github.com/songinyong/MobileX/assets/30370933/34db4764-471a-4646-ae8f-b47612245d7e)

https://www.semianalysis.com/p/google-we-have-no-moat-and-neither


Google's research findings indicate that open-source Large Language Models (LLMs) are experiencing rapid performance improvements. I will now explain the reasons behind these advancements in English for your students.

LLMs on a Phone: Today, people can run foundation models on devices like the Pixel 6 at a speed of 5 tokens per second. This remarkable achievement is due to the continuous optimization of algorithms and hardware, allowing powerful AI models to be run on mobile devices.

Scalable Personal AI: It is now possible to fine-tune personalized AI models on a laptop in just one evening. This is a result of increased accessibility and user-friendliness of AI tools, which enables more people to customize AI solutions to their specific needs without requiring vast computational resources.

Responsible Release: Although the issue of responsible release isn't entirely solved, it is becoming less relevant as open-source platforms provide unrestricted access to a wide array of art and text models. This development has democratized access to AI technologies and encourages creativity and innovation in the field.

Multimodality: State-of-the-art multimodal models, like ScienceQA, can be trained in just an hour. This achievement is due to the efficient combination of various data modalities and the development of more effective training techniques.

Overall, the rapid advancements in open-source LLMs can be attributed to continuous optimization, increased accessibility, democratization of AI technologies, and the development of efficient training techniques. These factors have greatly contributed to the performance improvements observed in open-source AI models.


## Model to use in the practice


![image](https://github.com/songinyong/MobileX/assets/30370933/c4863554-a964-4877-92b6-c9a745b03d75)

https://github.com/melodysdreamj/WizardVicunaLM


WizardVicuna is an improved LLM model that provides excellent support for foreign languages, including Korean. As a model currently deployed on the TRIPTON server, your goal is to utilize the knowledge gained from previous exercises to create and run a chatbot server locally, leveraging the capabilities of the WizardVicuna model.


## Performance Requirements for Hands-on Exercises

7B => ~4 GB

13B => ~8 GB

30B => ~16 GB

65B => ~32 GB

In Exercise 1, you have experienced running a 4-bit quantized chatbot locally. The original models typically operate using 32-bit floating-point numbers by default, which means that the inference of the original model would require at least 8 times more memory than what is listed in the table above.

For instance, if a model is over 50GB in size likes Vicunna13B, additional memory is needed during the inference process. This is because the original model, with its 32-bit floating-point representation, requires more memory to store the intermediate states and results during computation.

Furthermore, when it comes to training, even larger memory capacities are necessary due to factors such as batch size. A larger batch size means that more data points are processed simultaneously, which in turn requires more memory to store the gradients, activations, and other intermediate values. As a result, the actual memory requirements for training can be significantly higher than those for inference.

Furthermore, when it comes to training, even larger memory capacities are necessary due to factors such as batch size. A larger batch size means that more data points are processed simultaneously, which in turn requires more memory to store the gradients, activations, and other intermediate values. As a result, the actual memory requirements for training can be significantly higher than those for inference.

For example, the Alpaca 7B model required four A100 GPUs during training, and even the relatively memory-efficient fine-tuning process necessitated approximately 112GB or more of memory.

Operating unquantized original LLM models is still burdensome for individuals due to their substantial memory requirements.

Therefore, the goal of this hands-on exercise is to easily perform inference tasks using the pre-configured 13B Wizard-Vicunna Model on the TRIPTON server, enabling a more accessible experience for users.

