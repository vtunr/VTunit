# VTunit and ESP    
This container is to use when unit testing code on ESP32 as you need to generate a sdkconfig.h so you need the full toolchain to be working.

Run it the same way as the docker for VTunit only : 

```
docker run --name vtunit_esp --rm -v ${PWD}:/project -v /project/ -t vtunr/vtunit_esp:latest python -m vtunit unit_test/ build --cmake --run
```