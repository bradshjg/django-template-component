import dataclasses

from django.shortcuts import render


@dataclasses.dataclass(frozen=True)
class MockProfile:
    avatar_url: str
    title: str
    about_me: str
    show_contact_info: bool = False


@dataclasses.dataclass(frozen=True)
class MockUser:
    name: str
    email: str
    profile: MockProfile
    is_staff: bool = False

    def get_full_name(self) -> str:
        return self.name


def template_user_details(request):
    user = MockUser(
        name="jack",
        email="jack@example.com",
        profile=MockProfile(avatar_url="https://avatars.com/jack", title="jack's profile", about_me="just jack"),
    )
    viewer = MockUser(
        name="diane",
        email="diane@example.com",
        profile=MockProfile(avatar_url="https://avatars.com/diane", title="diane's profile", about_me="just diane"),
    )
    return render(request, "component_test_app/template_user_details.html", {"user": user, "viewer": viewer})


def component_user_details(request):
    user = MockUser(
        name="jack",
        email="jack@example.com",
        profile=MockProfile(avatar_url="https://avatars.com/jack", title="jack's profile", about_me="just jack"),
    )
    viewer = MockUser(
        name="diane",
        email="diane@example.com",
        profile=MockProfile(avatar_url="https://avatars.com/diane", title="diane's profile", about_me="just dian"),
    )
    return render(request, "component_test_app/component_user_details.html", {"user": user, "viewer": viewer})


def component_testing(request, *, template):
    template_name = f"component_test_app/{template}.html"
    return render(request, template_name)
