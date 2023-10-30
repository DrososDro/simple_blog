from django import forms

from blog_posts.models import BlogPost


class PostsForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ["title", "content"]

    def __init__(
        self,
        data=None,
        files=None,
        auto_id="id_%s",
        prefix=None,
        initial=None,
        error_class=...,
        label_suffix=None,
        empty_permitted=False,
        instance=None,
        use_required_attribute=None,
        renderer=None,
    ):
        super().__init__(
            data,
            files,
            auto_id,
            prefix,
            initial,
            error_class,
            label_suffix,
            empty_permitted,
            instance,
            use_required_attribute,
            renderer,
        )

        for name, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class": "w-36 rounded-xl px-5 py-2 leading-3 outline-none transition-all duration-500 focus:ring md:w-full bg-stone-100"
                }
            )
