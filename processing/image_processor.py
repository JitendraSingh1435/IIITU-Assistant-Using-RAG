from PIL import Image
import requests
from transformers import BlipProcessor, BlipForConditionalGeneration
from transformers import CLIPProcessor, CLIPModel
import torch

# Load models once
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")


def generate_caption(image_url):
    try:
        image = Image.open(requests.get(image_url, stream=True).raw).convert('RGB')

        inputs = blip_processor(images=image)
        out = blip_model.generate(**inputs)

        caption = blip_processor.decode(out[0], skip_special_tokens=True)
        return caption

    except:
        return ""


def get_clip_embedding(image_url):
    try:
        image = Image.open(requests.get(image_url, stream=True).raw).convert('RGB')

        inputs = clip_processor(images=image)
        outputs = clip_model.get_image_features(**inputs)

        return outputs.detach().numpy()

    except:
        return None