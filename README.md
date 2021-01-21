# tfl
Listing resources of terraform files without state.

## Usage
default format.

```terminal
$ cd (Your terraform workspace)

$ python tfl.py -d ./
# aws_alb
- ...

# aws_instance
- ...

# (ResourceType)
- (ResourceName)
- ...
```

format to use terraform plan `-target` option.

```
$ python tfl.py -d ./ --use-target
-target=aws_alb.xxx
-target=aws_alb.yyy
-target=aws_instance.foo
-target=aws_instance.bar
```

## license
[MIT](LICENSE)
