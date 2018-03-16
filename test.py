from lzwencoder import (
    LzwEncoder
)
from main_dictionary import (
    main_dictionary
)

lzw = LzwEncoder(main_dictionary)
test_string = "TOBEORNOTTOBEORTOBEORNOT#"
encoded_string = lzw.encode(test_string)
decoded_string = lzw.decode(encoded_string)
lzw.test_result(test_string, encoded_string, decoded_string)

test_string = "TESTINGALNGSTRINGTOSEEIFITEVERFAILSTESTINGALONGFAILSTOSEEIFITFAILSTESTINGALNGSTRINGTOSEEIFITEVERFAILS#"
encoded_string = lzw.encode(test_string)
decoded_string = lzw.decode(encoded_string)
lzw.test_result(test_string, encoded_string, decoded_string)
