# SWIM deployment

## Prerequisites
Before start make sure the following software is installed on your machine:
    
   - [git](https://git-scm.com/downloads)
   - [docker](https://docs.docker.com/install/)
   - [docker-compose](https://docs.docker.com/compose/install/)

### Preparation

#### Download repositories
First you need to clone the repositories in the current directory
```shell
git clone https://antavelos-eurocontrol@bitbucket.org/antavelos-eurocontrol/subscription-manager.git &&
git clone https://antavelos-eurocontrol@bitbucket.org/antavelos-eurocontrol/swim-adsb.git &&
git clone https://antavelos-eurocontrol@bitbucket.org/antavelos-eurocontrol/swim-explorer.git
```

#### Configuration
##### Environment variables
Make sure that the following enviroment variables are set. (You may choose different values)
```shell
export SM_ADMIN_USERNAME=admin    
export SM_ADMIN_PASSWORD=admin
export SWIM_ADSB_USERNAME=swim-adsb
export SWIM_ADSB_PASSWORD=swim-adsb
export SWIM_EXPLORER_USERNAME=swim-explorer
export SWIM_EXPLORER_PASSWORD=swim-explorer
```
##### Config files


### Deployment

```shell
docker-compose p -d
```