from discord.ext import commands


def has_any_role(*roles):
    async def predicate(ctx: commands.Context):
        return any(role.name in roles for role in ctx.author.roles)

    return commands.check(predicate)


def has_all_roles(*roles):
    async def predicate(ctx: commands.Context):
        user_roles = {role.name for role in ctx.author.roles}
        return all(role in user_roles for role in roles)

    return commands.check(predicate)


def has_roles_or_permissions(roles, **permissions):
    async def predicate(ctx: commands.Context):
        # Check for roles
        has_role = any(role.name in roles for role in ctx.author.roles)
        # Check for permissions
        has_permission = all(getattr(ctx.author.guild_permissions, perm, None) for perm in permissions)
        return has_role or has_permission

    return commands.check(predicate)
