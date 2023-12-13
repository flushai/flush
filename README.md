# [Flush AI](https://flushai.cloud)


## ⚡ Quick Install

`pip3 install flushai`

## 📖 Documentation

[https://docs.flushai.cloud](https://docs.flushai.cloud)

## 🏷 What is Flush AI

Flush AI is an SDK for generative Image AI models, designed to help developers easily create advanced, multi-modal generative AI-driven applications. We allow developers to create 'chains', integrating various models together. Developers can chain together LLMs and any model hosted on our platform - along with our data integrations - to create multi-modal workflows between these models.

Stay updated with Flush AI on our [twitter](https://twitter.com/flush_ai) or join our community on [discord](https://discord.gg/flushai). Follow our [instagram](https://www.instagram.com/flush.ai/) and our [tiktok](https://www.tiktok.com/@flush.ai) for cool art generated on our platform.

# Get Started with Flush AI
Here are a few quick steps to get Flush AI integrated into your projects.

After installing Flush AI, you can start building your chains by integrating various models. For example, here is how you can chain together LLMs like GPT-4 and Stable Diffusion XL to create generate images using enhanced prompts.

First, let us import all the required dependencies and initialize our base models.
```python
from flushai import Chain
from flushai.models.llms import OpenAI
from flushai.models.diffusion.text2img import StableDiffusionXL

llm = OpenAI(model_name="gpt-4", api_key="YOUR_OPENAI_API_KEY")
diffusion = StableDiffusionXL(api_key="YOUR_API_KEY")
```

We can configure a prompt template for how we want GPT-4 to generate prompts:
```python
from flushai.prompts import PromptTemplate

prompt = '''
(subject of the image), (5 descriptive keyword), (camera type), 
(camera lens type), (time of day), (style of photography), 
(type of film), (Realism Level), (Best type of lighting for the subject).

Based on the above structure, create a detailed narrative of the scene in 20 
words. Generate only 1 variation. Return strictly only the narrative. Subject 
of the prompt is: {subject}
'''

prompt_template = PromptTemplate(prompt)
```

We can specify the chain like such:

```python
params = {
    "num_images": 1
}

chain = Chain(
    llm_output = (llm, prompt_template),
    diffusion_output = (diffusion, "{llm_output}", params)
)
```

You can specify different subjects as per your Prompt Template. To run the chain, simply run:

```python
chain.run(subject="urban photography")
```

You can instruct GPT-4 to create different types of prompts based on your message to it. You can specify styles, the token length, subjects, or anything else and with Flush's chains, you can build powerful applications. For more details on using our data integrations and other use cases of Flush, check out our [docs](https://docs.flushai.cloud/introduction)

---
## Support
Flush AI is continuously evolving, and we appreciate community involvement. We welcome all forms of contributions - bug reports, feature requests, and code contributions.

1. Report bugs and request features by opening an [issue](https://github.com/flushai/flush/issues) on Github.
2. Contribute to the project by forking the repository and submitting a pull request with your changes.
