#!/usr/bin/env python

from mpi4py import MPI
import sys, datetime, os
from contract import generate_AES_key, divide_key_into_segments, create_fragment_identifiers, distribute_key_fragments
import sys
sys.path.append('/key-generation')
sys.path.append('/key-send')


def dc_2pqc(data_chunk, output_path):
    comm = MPI.COMM_WORLD
    rank = MPI.COMM_WORLD.Get_rank()
    size = MPI.COMM_WORLD.Get_size()

    ##################
    # Phase 1: Prepare
    ##################

    # Broadcasting prepare message
    prepare_msg = comm.bcast("PREPARE", root=0)

    # Sending prepare readiness
    ready_to_prepare = 1  # 1: Ready; 0: Not Ready
    ready = comm.gather(ready_to_prepare, root=0)

    # Gathering prepare readiness from all nodes
    if rank == 0:
        if sum(ready) == size:
            commit_decision = True  # Consensus to commit
        else:
            commit_decision = False  # Consensus not reached
        comm.bcast(commit_decision, root=0)

    # Check commit decision
    commit_decision = comm.bcast(None, root=0)

    #################
    # Phase 2: Commit
    #################

    if commit_decision:
        # Local Commit
        if rank == 0:
            with open(os.path.join(output_path, f"log_{rank}.txt"), "a+") as file:
                file.write(f"log_{rank} at {datetime.datetime.now()}: {data_chunk}\n")
        # Sending local commit status to the root process
        local_commit_status = 1
    else:
        # Sending local abort status to the root process
        local_commit_status = 0

    # Gathering local commit status from all nodes
    commit_status = comm.gather(local_commit_status, root=0)

    # Reporting the final result of the transaction
    if rank == 0:
        if sum(commit_status) >= size / 2:
            sys.stdout.write("Transaction committed successfully.\n")
        else:
            sys.stdout.write("Transaction failed to commit.\n")

# All the existing code from dc_2pqc to commit_txn remains unchanged
# Function to achieve consensus using 2-Phase Commit Protocol
def achieve_consensus(data_chunk, output_path):
    # Your code here to initiate 2-Phase Commit Protocol for achieving consensus
    dc_2pqc(data_chunk, output_path)

# Entry point
if __name__ == '__main__':

    # Your existing code remains the same

    # Generate AES key
    generated_key = generate_AES_key()

    # Divide key into segments
    segmented_keys = divide_key_into_segments(generated_key)

    # Create fragment identifiers
    fragment_identifiers = create_fragment_identifiers(data_chunk, segmented_keys)

    # Distribute key fragments among blockchain sub-cluster
    distribute_key_fragments(fragment_identifiers, segmented_keys)

   # Perform operations to submit transaction, process, and commit
    for i in range(10000): 
        received_txn = submit_txn(txn + str(i))
        
        if __debug__: 
            sys.stdout.write("received_txn = %s received at rank %d \n" % (received_txn, rank))

        # Process the transaction on all nodes
        process_txn()

        # Achieve consensus using 2-Phase Commit Protocol
        achieve_consensus(received_txn, output_path)
