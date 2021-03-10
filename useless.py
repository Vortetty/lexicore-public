import pkg_resources

installed_packages = pkg_resources.working_set
installed_packages_list = sorted([i.key
   for i in installed_packages])
print(installed_packages_list)

e = help("modules")