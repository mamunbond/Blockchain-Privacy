from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.rank
size = comm.size

def main():
    if 0 <= rank < 125:
        shared = {'d1': 55}
        for i in range(1, 125):
            comm.send(shared, dest=i)
    elif 125 <= rank < 250:
        shared = {'d1': 55}
        for i in range(125, 250):
            comm.send(shared, dest=i)
    elif 250 <= rank < 375:
        shared = {'d2': 42}
        for i in range(250, 375):
            comm.send(shared, dest=i)
    elif 375 <= rank < 500:
        shared = {'d2': 42}
        for i in range(375, 500):
            comm.send(shared, dest=i)
    else:
        if rank == 0:
            shared = {'d1': 55}
            for i in range(1, size):
                comm.send(shared, dest=i)
        elif 125 <= rank < 250:
            shared = {'d1': 55}
            for i in range(125, size):
                comm.send(shared, dest=i)
        elif 250 <= rank < 375:
            shared = {'d2': 42}
            for i in range(250, size):
                comm.send(shared, dest=i)
        elif 375 <= rank < 500:
            shared = {'d2': 42}
            for i in range(375, size):
                comm.send(shared, dest=i)

    if rank < 125:
        receive = comm.recv(source=0)
        print("Key:", receive, "received at node", rank)
    elif 125 <= rank < 250:
        receive = comm.recv(source=125)
        print("Key:", receive, "received at node", rank)
    elif 250 <= rank < 375:
        receive = comm.recv(source=250)
        print("Key:", receive, "received at node", rank)
    elif 375 <= rank < 500:
        receive = comm.recv(source=375)
        print("Key:", receive, "received at node", rank)

if __name__ == '__main__':
    main()
