# Contributing modules to CFEngine Build

## Development

We recommend using this template as a starting point when creating your first module:

https://github.com/cfengine/module-template

### Testing

The module template, or your version of it can be tested as if you were a user of the module:

```
mkdir new_test_repo
cd new_test_repo
cfbs init
cfbs add mpf
cfbs add https://github.com/cfengine/module-template
cfbs build
```

### Requirements

* Some reusable module code you want to share
  * Can be a policy file, a promise type written in python, etc.
  * Must be reusable, other users must be able to use it without editing it. [Augments](https://docs.cfengine.com/docs/master/reference-language-concepts-augments.html) provide a way for users to override defaults in policy.
* A `cfbs.json` project file
  * Enables others to do `cfbs add <your repo url>` to test your module even before it is in the index
* A README file
  * Must contain some basic information about what your module does and how to use it
  * If your module requires some data or additional steps clearly tell your users what they need to do
  * Can use [this README](https://github.com/cfengine/modules/blob/master/promise-types/git/README.md) as an example to follow

## Publishing your module for others to reuse

When your module is working and ready for others to use, you can submit a pull request to change the index of CFEngine Build modules:

https://github.com/cfengine/build-index/blob/master/cfbs.json

(Submit a pull request to master branch, either by editing the file in GitHub UI, or cloning and editing locally).

Your entry inside the `index` should have the following contents, in this order:
* A unique key - the name of the module
* `"description"` (string) - Explains what the module does
* `"tags"` (list of strings) - Used to group the modules on the website
* `"repo"` (string) - URL to the repository to fetch your module from
* `"by"` (string) - URL to the GitHub user which should show up as the author
* `"version"` (string) - Version number of your module, 3 numbers separated by dots
* `"commit"` (string) - Commit SHA of your module
* `"subdirectory"` (optional, string) - Subdirectory inside repo which has that module
* `"dependencies"` (optional, list of strings) - What other modules in the index are required for your module to work
* `"steps"` (list of strings) - What steps should be run when a user runs `cfbs build` after adding your module

People from the CFEngine team will review your module, and might have some feedback on things you could improve.
After being reviewed and approved, the change in the index will be merged, and your new version will be available shortly.

Note that the CFEngine team may in some cases decide to not include a module in the index and on our website.
In this case you can still share it with others, they just have to add it using the full URL.

## Publishing updates

When your module is already in the CFEngine Build index and you've been working on a new update, you can submit an update to your module.
This is done by editing [the index file](https://github.com/cfengine/build-index/blob/master/cfbs.json) and submitting a pull request.
You must update both `version` and `commit` (you can also update other parts if necessary, such as `steps`).
It should look something like this:

https://github.com/cfengine/build-index/pull/52/files

You can write a short changelog describing what was changed.

## Getting help

If you have a question, find something unclear, or need help with CFEngine Build, feel free to submit a question to our GitHub Discussions:

https://github.com/cfengine/core/discussions/categories/q-a
