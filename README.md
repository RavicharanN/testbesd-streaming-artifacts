## ML Flow 

This repository serves as a demonstration of a data streaming pipeline involving the simulation of real-time streaming events. The pipeline is built using a static object store and employs Redpanda as the messaging system for producer-consumer interactions.

## Setting up the VMs on Chameleon Cloud

This experiment assumes you have already completed  [Hello, Chameleon](https://teaching-on-testbeds.github.io/blog/hello-chameleon), so you have set up your Chameleon account, created and added keys to your account, and joined an active project on Chameleon.

Running the  `reserve_chameleon.ipynb` notebook intiatialize the 3 node setup for you to run your experiments. From the [Chameleon website](https://chameleoncloud.org/), click on "Experiment > Jupyter Interface" in the menu. You may be prompted to log in. You will then upload the `reserve_chameleon.ipynb` and run all cells to launch the VMs

If your notebook runs without any issues you will see an output in the "Network Topolgy" section that looks like this:

![Network Topology](./images/nettop.png)


* Node0 - TODO: Apache Flink
* Node1: Serves as the Minio Store
* Node2: Serves as the Postgres Store

Note: Currently we run both producer and consumer on node-1 but will be moved out that host in the final repo 

## Set up MinIO artifact store on Node 1

  

On node1 we will set up MinIO, an S3-compatible object storage, as an artifact store so that you don’t need to have AWS account to run this experiment. We will move the docker-compose files to node1 in a similar way we did for node 1.

  

Navigate to the directory where the docker-compose-minio.yaml file is located and run

  

```

scp -i <path to your private key> docker-compose-minio.yaml cc@your_public_ip:/home/

```

  

Then on node-0 run:

  

```

scp /home/docker-compose-minio.yaml node-1:/home/

```

  

Finally, on node-1 run:

```

docker compose -f /home/docker-compose-minio.yaml up -d

```

  

This will create an artifact store and also initialize and empty bucket named `flight-info` on node1

## Setting up Postgres server on Node 2

The Docker Compose file required to set up the Postgres database is provided in this repository. First, navigate to the directory where the docker-compose-postgres.yaml file is located. Since Node 0 is the only node exposed to the public, you must transfer the file to Node 0 first and then forward it to Node 2.

```
scp -i <path to your private key> postgres/docker-compose-postgres.yaml cc@your_public_ip:/home/
```

This will move the YAML file to node 0. Then on node 0 run: 

```
scp  /home/docker-compose-postgres.yaml node-2:/home/
```

Finally on node-2 run 
```
docker compose -f /home/docker-compose-postgres.yaml up -d
```

You can do a `docker ps` to check if the postgres server is succesfully up and running. 


This material is based upon work supported by the National Science Foundation under Grant No. 2230079.