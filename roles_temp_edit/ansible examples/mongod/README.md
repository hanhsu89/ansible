
1. Khởi tạo Replication trên Master
   ```bash
   > rs.initiate()
   ```
2. Add/Remove Replication
   ```bash
   PRIMARY> rs.add('mongo2.appconus.com:27017')
   PRIMARY> rs.remove('mongo2.appconus.com:27017')
   ```
3. Add Arbitrator
   ```bash
   PRIMARY> rs.addArb('mongo3.appconus.com:27017')
   ```
4. Troubleshoot Replications
    ```bash
    PRIMARY> rs.config()
    PRIMARY> rs.status()

    SECONDARY> rs.slaveOk()
    SECONDARY> show dbs

    SECONDARY> rs.printSlaveReplicationInfo()
    #Check current start slave vs master

    SECONDARY> rs.status()
    # check optime , optimeDate, stateStr, lastHeartbeatMessage
    ```

5. Check storageEngine

    ```bash
    db.serverStatus().storageEngine
    db.serverStatus().wiredTiger
    ```
6. Get User in DB

    ```bash
    SECONDARY> use database
    SECONDARY> db.getUsers()
    ```