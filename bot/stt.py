import torch
import zipfile
import torchaudio
from glob import glob


device = torch.device('cpu')
model, decoder, utils = torch.hub.load(
    repo_or_dir='snakers4/silero-models',
    model='silero_stt',
    language='en',
    device=device
)
(
    read_batch, split_into_batches,
    read_audio, prepare_model_input
) = utils


def voice_to_text(path_to_file):
    file = glob(path_to_file)
    batches = split_into_batches(file, batch_size=10)
    model_input = prepare_model_input(read_batch(batches[0]), device=device)

    output = model(model_input)
    result = []
    for elem in output:
        result.append(elem)
    return ' '.join(result)
