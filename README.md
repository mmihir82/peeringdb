## PeeringDB BGP Configure Genereator
Following steps to run the code:
```
  git clone https://github.com/mmihir82/peeringdb.git
  cd peeringdb
  docker build -t peeringdb .
  TO RUN THE PYTHON SCRIPT
      docker run --rm -v $(pwd)/log:/log peeringdb 22697
```
