# Considerations

1. request.json() loads all data to the RAM.<br>
2. Although uuid.UUID validates uuid, it allows alternative uuid representations.<br>
It can cause consistency problems.<br>
For example:

<pre>
import uuid


if __name__ == '__main__':
    uuid_representation = str(uuid.uuid4())
    uuid.UUID(uuid_representation)

    uuid_representation_that_can_cause_consistency_problems = (
        str(uuid.uuid4()).replace('-', '')
    )
    uuid.UUID(uuid_representation_that_can_cause_consistency_problems)
</pre>
