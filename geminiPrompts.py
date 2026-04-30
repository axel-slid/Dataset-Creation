# Mainly participants, with small amount of non-participants
SOME_NON_PROMPT = """Edit this image to create a realistic workplace scene for a participant-vs-non-participant dataset.

Goal:
Insert people into the existing room while preserving the original architecture, camera angle, furniture placement, lighting, perspective, and overall layout.

Requirements:
- Add 3 to 6 people inside the main meeting area.
- These people must clearly appear to be active meeting participants.
- Participants should look engaged in a shared discussion: talking, listening, gesturing, looking at each other, looking at a laptop/screen/notebook, taking notes, or presenting.
- Place participants naturally around tables, chairs, whiteboards, or presentation areas that already exist in the room.
- Make the interaction look coherent, as if they are part of the same meeting.
- The meeting should take place close to the camera.

Also:
- Add 1 to 3 additional visible people who are NOT part of the meeting.
- These non-participants must be spatially separate from the main meeting interaction.
- They can be standing near a hallway, outside the central table cluster, passing by, waiting, using a phone, walking in the background, talking to each other, or working independently.
- They must remain visible, but should not visually dominate the scene.
- They must not appear engaged with the meeting participants.

Constraints:
- Do not change the room layout.
- Do not add or remove walls, windows, doors, tables, or major furniture.
- Do not change the camera viewpoint or crop.
- Do not turn the room into a different space.
- Maintain realistic scale, body proportions, occlusion, shadows, and perspective.
- Keep the final result photorealistic and consistent with the original image.
- Avoid crowding the room too heavily.
- Avoid duplicated-looking people or obviously staged poses.
- It should NOT be ambiguous who is in a meeting and who is not.

Dataset intent:
The final image should make it easy to distinguish:
1. meeting participants involved in the central collaborative activity
2. visible non-participants who are present in the scene but not involved in the meeting
"""
# All people are participants
NO_NON_PROMPT = """Edit this image to create a realistic workplace scene for a participant-vs-non-participant dataset.

Goal:
Insert people into the existing room while preserving the original architecture, camera angle, furniture placement, lighting, perspective, and overall layout.

Requirements:
- Add 3 to 6 people inside the main meeting area.
- These people must clearly appear to be active meeting participants.
- Participants should look engaged in a shared discussion: talking, listening, gesturing, looking at each other, looking at a laptop/screen/notebook, taking notes, or presenting.
- Place participants naturally around tables, chairs, whiteboards, or presentation areas that already exist in the room.
- Make the interaction look coherent, as if they are part of the same meeting.
- With 80 percent chance, have everyone sitting. With 20 percent chance, have at least one person standing. Ensure they are a natural part of the meeting. 

Constraints:
- Do not change the room layout.
- Do not add or remove walls, windows, doors, tables, or major furniture.
- Do not change the camera viewpoint or crop.
- Do not turn the room into a different space.
- Maintain realistic scale, body proportions, occlusion, shadows, and perspective.
- Keep the final result photorealistic and consistent with the original image.
- Avoid crowding the room too heavily.
- Avoid duplicated-looking people or obviously staged poses.
"""

MOST_NON_PROMPT = """Edit this image to create a realistic workplace scene for a participant-vs-non-participant dataset.

Goal:
Insert people into the existing room while preserving the original architecture, camera angle, furniture placement, lighting, perspective, and overall layout.

Requirements:
- Add 3 to 6 people inside the main meeting area.
- These people must clearly appear to be active meeting participants.
- Participants should look engaged in a shared discussion: talking, listening, gesturing, looking at each other, looking at a laptop/screen/notebook, taking notes, or presenting.
- Place participants naturally around tables, chairs, whiteboards, or presentation areas that already exist in the room.
- Make the interaction look coherent, as if they are part of the same meeting.
- The meeting should take place close to the camera.

Also:
- Add 5-20 additional visible people who are NOT part of the meeting, naturally filling the rest of the image.
- These non-participants must be spatially separate from the main meeting interaction.
- They can be standing near a hallway, outside the central table cluster, passing by, waiting, using a phone, walking in the background, talking to each other, or working independently.
- They must remain visible, but should not visually dominate the scene.
- They must not appear engaged with the meeting participants.

Constraints:
- Do not change the room layout.
- Do not add or remove walls, windows, doors, tables, or major furniture.
- Do not change the camera viewpoint or crop.
- Do not turn the room into a different space.
- Maintain realistic scale, body proportions, occlusion, shadows, and perspective.
- Keep the final result photorealistic and consistent with the original image.
- Avoid crowding the room too heavily.
- Avoid duplicated-looking people or obviously staged poses.
- It should NOT be ambiguous who is in a meeting and who is not.

Dataset intent:
The final image should make it easy to distinguish:
1. meeting participants involved in the central collaborative activity
2. visible non-participants who are present in the scene but not involved in the meeting
"""
