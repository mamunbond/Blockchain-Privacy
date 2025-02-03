from Crypto.Cipher import AES
import base64, os
from mpi4py import MPI
import time

def current_time_ms():
    return time.time() * 1000

def generate_secret_key_for_AES_cipher():
    # AES key length must be either 16, 24, or 32 bytes long
    AES_key_length = 16 # use larger value in production
    # generate a random secret key with the decided key length
    # this secret key will be used to create AES cipher for encryption/decryption
    secret_key = os.urandom(AES_key_length)
    # encode this secret key for storing safely in database
    encoded_secret_key = base64.b64encode(secret_key)
    return encoded_secret_key

####### BEGIN HERE #######

def main():
    comm = MPI.COMM_WORLD
    rank = comm.rank
    size = comm.size

    private_msg = """
    Lorem ipsum dolor sit amet, malis recteque posidonium ea sit, te vis meliore verterem. Duis movet comprehensam eam ex, te mea possim luptatum gloriatur. Modus summo epicuri eu nec. Ex placerat complectitur eos.
    """
    padding_character = "{"
    time1 = 0
    time2 = 0
    n = 20  # data chunks

    time1 = current_time_ms()
    for j in range(rank, n*size, size):
        f = open("keylist.txt", "a")
        secret_key = generate_secret_key_for_AES_cipher()
        f.write("   Secret Key: %s - (%d)\n" % (secret_key, len(secret_key)))
        f.close()
    time2 = current_time_ms()

    totaltime = time2 - time1
    file_size = os.path.getsize('keylist.txt')
    
    comm.barrier()  # Ensure all processes have completed writing before calculating the total size
    total_file_size = comm.allreduce(file_size, op=MPI.SUM)

    if rank == 0:
        print("Data chunks ", n*size, "keys are of: ", total_file_size, "bytes")
        print("Time for", n*size, "keys registration: ", totaltime)

    with open("keylist.txt", 'r+') as f:
        f.truncate(0)

if __name__ == '__main__':
    main()
