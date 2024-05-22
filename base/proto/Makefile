common_pb2.py: common.proto
	protoc --python_out=.  --csharp_out=. $^

clean:
	rm -rf *_pb2.py *.cs
