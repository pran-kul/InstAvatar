from PIL import Image

# Load the maps
diffuse_map = Image.open('./output/PranavImage.png/diffuseMap_0.png')
specular_map = Image.open('./output/PranavImage.png/specularMap_0.png')
roughness_map = Image.open('./output/PranavImage.png/roughnessMap_0.png')

# Resize the maps to the same size
size = (max(diffuse_map.size, specular_map.size, roughness_map.size))
diffuse_map = diffuse_map.resize(size)
specular_map = specular_map.resize(size)
roughness_map = roughness_map.resize(size)

# Combine the maps into a single image
texture = Image.merge("RGB", (diffuse_map.convert("L"), specular_map.convert("L"), roughness_map.convert("L")))

# Save the texture
texture.save('./output/PranavImage.png/texture.png')