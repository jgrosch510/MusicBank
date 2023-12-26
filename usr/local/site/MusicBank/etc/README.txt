Files in this directory controls which tests are performed when comparing
database records. The test control files ar in the following form.

{ "tests": [
  { "position": 0,  "must_test": 1, "result": 0 },
  { "position": 1,  "must_test": 1, "result": 0 },
  { "position": 2,  "must_test": 1, "result": 0 },
]}

The title of the JSON structure must be "tests". Each line of the array has
3 elements; "position", "must_test", and "result". Position relates to the
defines in the class which represents the order of fields in the database
table. They _MUST_ be in numerical order. 

The second element is "must_test". This controls wether or not a test is
performed on a field. A 1 means yes as in yes, do the test. A 0 means no as
in no do not perform the test.

The third element is "reult". This is where the result of the test is
stored. Again a 1 means yes as in yes, do the test. A 0 means no as
in no do not perform the test. This field is used to report back how things
went and helps control futher actions by the class.