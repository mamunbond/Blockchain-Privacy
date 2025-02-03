from mpi4py import MPI
import random
import string
from Crypto.Cipher import AES
import base64, os
import time

def current_time_ms():
    return time.time() * 1000

    
comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# Function to generate key
def generate_key():
   # AES key length must be either 16, 24, or 32 bytes long
    AES_key_length = 16 # use larger value in production
    # generate a random secret key with the decided key length
    # this secret key will be used to create AES cipher for encryption/decryption
    secret_key = os.urandom(AES_key_length)
    # encode this secret key for storing safely in database
    encoded_secret_key = base64.b64encode(secret_key)
    return encoded_secret_key
    # # Generate a random key of length 16 composed of alphanumeric characters
    # key_length = 16
    # key = ''.join(random.choices(string.ascii_letters + string.digits, k=key_length))
    
    # if rank == 0:
    #     return key  # Generating the key only in the root process (rank 0)
    # else:
    #     return None

# Function to divide key into geometric segments (rectangle)
def divide_key_into_segments(key):
    # Splitting the key into segments (rectangle) - dividing it into 4 segments
    segmented_keys = [key[i:i+len(key)//4] for i in range(0, len(key), len(key)//4)]
    return segmented_keys

# Function to create key fragment identifiers
def create_fragment_identifiers(block, key_segments):
    # Creating fragment identifiers for association with block and key segments
    fragment_identifiers = [f"Fragment_{i+1}_of_Block_{block}" for i in range(len(key_segments))]
    return fragment_identifiers

# Function to distribute key fragments among blockchain sub-cluster using MPI
def distribute_key_fragments(fragment_ids, key_segments):
    # Distributing key fragments among blockchain sub-clusters using MPI
    for fragment_id, key_segment in zip(fragment_ids, key_segments):
        print(f"Process {rank} - Distributing fragment {fragment_id} with key segment: {key_segment}")

# Function representing the ZTP-Key-Dist algorithm using MPI
def ztp_key_distribution(blockchain_nodes, data_chunk, geometric_shape, chunk_size, redundancy):
    # Generate the key
    key = generate_key()

    # Broadcast the key to all processes in the communicator
    key = comm.bcast(key, root=0)

    # Divide the key into geometric segments (rectangle)
    segmented_keys = divide_key_into_segments(key)

    # Create key fragment identifiers
    fragment_identifiers = create_fragment_identifiers(data_chunk, segmented_keys)

    # Distribute key fragments among blockchain sub-cluster using MPI
    distribute_key_fragments(fragment_identifiers, segmented_keys)

    # Return the segmented data chunks, fragment identifiers, segmented keys
    return segmented_keys, fragment_identifiers, segmented_keys


#segmented_chunks, fragment_ids, keys = ztp_key_distribution(blockchain_nodes, data_chunk, geometric_shape, chunk_size, redundancy)
