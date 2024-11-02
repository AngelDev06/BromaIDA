import re

def main(target_name: str):
    patch_classes = (
        "GameObjectEditorState",
        "GJValueTween",
        "SongChannelState",
        "GJPointDouble",
        "GameObjectPhysics"
    )
    
    with open(target_name) as file:
        content = file.read()
    
    for patch_class in patch_classes:
        class_decl_pattern = re.compile(
            r"""
                (?P<declaration>
                    (?:class|struct)\s+
                    {}
                )\s*;
            """.format(patch_class),
            re.X
        )
        class_def_pattern = re.compile(
            r"""
                (?P<declaration>
                    (?:class|struct)\s+
                    {}
                )\s*
                (?P<definition>\{{.*?}};)
            """.format(patch_class),
            re.X | re.DOTALL
        )
        
        matched = class_def_pattern.search(content)
        declaration = matched.group("declaration")
        definition = matched.group("definition")
        content = class_def_pattern.sub("", content, 1)
        content = class_decl_pattern.sub(f"{declaration}\n{definition}", content)
    
    with open(target_name, "w") as file:
        file.write(content)

if __name__ == "__main__":
    main("android64.hpp")
