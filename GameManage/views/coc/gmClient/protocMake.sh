#protoc -I=../../../src/proto/ --python_out=. ../../../src/proto/*.proto
protoc -I=./protocol/ --python_out=./protopy/ ./protocol/*.proto
