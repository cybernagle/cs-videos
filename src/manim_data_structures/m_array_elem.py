import numpy as np
from manim import *

from .m_enum import MArrayDirection, MArrayElementComp


class MArrayElement(VGroup):
    """A class that represents an array element.

    Parameters
    ----------
    mob_square_args : :class:`dict`, default: `{}`
        Arguments for :class:`manim.Square` that represents the element body.
    mob_value_args : :class:`dict`, default: `{}`
        Arguments for :class:`manim.Text` that represents the element value.
    mob_index_args : :class:`dict`, default: `{}`
        Arguments for :class:`manim.Text` that represents the element index.
    index_pos : :class:`np.ndarray`, default: `UP`
        Specifies the position of :attr:`__mob_index`
    index_gap : :class:`float`, default: `0.25`
        Specifies the distance between :attr:`__mob_square` and :attr:`__mob_index`
    label_pos : :class:`np.ndarray`, default: `LEFT`
        Specifies the position of :attr:`__mob_label`
    label_gap : :class:`float`, default: `0.5`
        Specifies the distance between :attr:`__mob_square` and :attr:`__mob_label`
    next_to_mob : :class:`MArrayElement`, default: `None`
        Specifies placement for :attr:`__mob_square`
    next_to_dir : :class:`np.ndarray`, default: `RIGHT`
        Specifies direction of placement for :attr:`__mob_square`

    Attributes
    ----------
    __mob_square_props : :class:`dict`
        Default arguments passed to :class:`manim.Square` that represents the element body.
    __mob_value_props : :class:`dict`
        Default arguments passed to :class:`manim.Text` that represents the element value.
    __mob_index_props : :class:`dict`
        Default arguments passed to :class:`manim.Text` that represents the element index.
    __mob_square : :class:`manim.Square`
        :class:`manim.Mobject` that represents the element body.
    __mob_value : :class:`manim.Text`
        :class:`manim.Mobject` that represents the element index.
    __mob_index : :class:`manim.Text`
        :class:`manim.Mobject` that represents the element value.
    __index_pos : :class:`np.ndarray`
        Specifies the position of :attr:`__mob_index`
    __index_gap : :class:`float`
        Specifies the distance between :attr:`__mob_square` and :attr:`__mob_index`
    __label_pos : :class:`np.ndarray`, default: `LEFT`
        Specifies the position of :attr:`__mob_label`
    __label_gap : :class:`float`, default: `0.5`
        Specifies the distance between :attr:`__mob_square` and :attr:`__mob_label`
    """

    def __init_props(
        self,
        index_pos: np.ndarray,
        index_gap: float,
        label_pos: np.ndarray,
        label_gap: float,
    ) -> None:
        """Initializes the attributes for the class.

        Parameters
        ----------
        index_pos : :class:`np.ndarray`
            Specifies the position of :attr:`__mob_index`
        index_gap : :class:`float`
            Specifies the distance between :attr:`__mob_square` and :attr:`__mob_index`
        label_pos : :class:`np.ndarray`
            Specifies the position of :attr:`__mob_label`
        label_gap : :class:`float`
            Specifies the distance between :attr:`__mob_square` and :attr:`__mob_label`
        """

        self.__mob_square_props = {
            "color": BLUE_B,
            "fill_color": BLUE_D,
            "fill_opacity": 1,
            "side_length": 1,
        }
        self.__mob_value_props = {"text": "", "color": WHITE, "weight": BOLD}
        self.__mob_index_props = {"text": "", "color": BLUE_D, "font_size": 32}
        self.__mob_label_props = {"text": "", "color": BLUE_A, "font_size": 38}
        self.__index_pos = index_pos
        self.__index_gap = index_gap
        self.__label_pos = label_pos
        self.__label_gap = label_gap

    def __update_props(
        self,
        mob_square_args: dict = {},
        mob_value_args: dict = {},
        mob_index_args: dict = {},
        mob_label_args: dict = {},
    ) -> None:
        """Updates the attributes of the class.

        Parameters
        ----------
        mob_square_args : :class:`dict`, default: `{}`
            Arguments for :class:`manim.Square` that represents the element body.
        mob_value_args : :class:`dict`, default: `{}`
            Arguments for :class:`manim.Text` that represents the element value.
        mob_index_args : :class:`dict`, default: `{}`
            Arguments for :class:`manim.Text` that represents the element index.
        mob_label_args : :class:`dict`, default: `{}`
            Arguments for :class:`manim.Text` that represents the element label.
        """

        self.__mob_square_props.update(mob_square_args)
        self.__mob_value_props.update(mob_value_args)
        self.__mob_index_props.update(mob_index_args)
        self.__mob_label_props.update(mob_label_args)

        if type(self.__mob_value_props["text"]) != str:
            self.__mob_value_props["text"] = str(self.__mob_value_props["text"])

        if type(self.__mob_index_props["text"]) != str:
            self.__mob_index_props["text"] = str(self.__mob_index_props["text"])

        if type(self.__mob_label_props["text"]) != str:
            self.__mob_label_props["text"] = str(self.__mob_label_props["text"])

    def __init_mobs(
        self,
        init_square: bool = False,
        init_value: bool = False,
        init_index: bool = False,
        init_label: bool = False,
        next_to_mob: "MArrayElement" = None,
        next_to_dir: np.ndarray = RIGHT,
    ) -> None:
        """Initializes the :class:`Mobject`s for the class.

        Parameters
        ----------
        init_square : :class:`bool`, default: `False`
            Instantiates a :class:`manim.Sqaure` and adds it to :attr:`__mob_square`.
        init_value : :class:`bool`, default: `False`
            Instantiates a :class:`manim.Text` and adds it to :attr:`__mob_value`.
        init_index : :class:`bool`, default: `False`
            Instantiates a :class:`manim.Text` and adds it to :attr:`__mob_index`.
        init_label : :class:`bool`, default: `False`
            Instantiates a :class:`manim.Text` and adds it to :attr:`__mob_label`.
        next_to_mob : :class:`MArrayElement`, default: `None`
            Specifies placement for :attr:`__mob_square`
        next_to_dir : :class:`np.ndarray`, default: `RIGHT`
            Specifies direction of placement for :attr:`__mob_square`
        """

        if init_square:
            self.__mob_square = Square(**self.__mob_square_props)
            if next_to_mob is not None:
                self.__mob_square.next_to(
                    next_to_mob.fetch_mob_square(), next_to_dir, 0
                )
            self.add(self.__mob_square)

        if init_value:
            self.__mob_value = Text(**self.__mob_value_props)
            self.__mob_value.next_to(self.__mob_square, np.array([0, 0, 0]), 0)
            self.add(self.__mob_value)

        if init_index:
            self.__mob_index = Text(**self.__mob_index_props)
            self.__mob_index.next_to(
                self.__mob_square, self.__index_pos, self.__index_gap
            )
            self.add(self.__mob_index)

        if init_label:
            self.__mob_label = Text(**self.__mob_label_props)
            self.__mob_label.next_to(
                self.__mob_square, self.__label_pos, self.__label_gap
            )
            self.add(self.__mob_label)

    def __init__(
        self,
        mob_square_args: dict = {},
        mob_value_args: dict = {},
        mob_index_args: dict = {},
        mob_label_args: dict = {},
        index_pos: np.ndarray = UP,
        index_gap: float = 0.25,
        label_pos: np.ndarray = LEFT,
        label_gap: float = 0.5,
        next_to_mob: "MArrayElement" = None,
        next_to_dir: np.ndarray = RIGHT,
        **kwargs
    ) -> None:
        """Initializes the class.

        Parameters
        ----------
        mob_square_args : :class:`dict`, default: `{}`
            Arguments for :class:`manim.Square` that represents the element body.
        mob_value_args : :class:`dict`, default: `{}`
            Arguments for :class:`manim.Text` that represents the element value.
        mob_index_args : :class:`dict`, default: `{}`
            Arguments for :class:`manim.Text` that represents the element index.
        mob_label_args : :class:`dict`, default: `{}`
            Arguments for :class:`manim.Text` that represents the element label.
        index_pos : :class:`np.ndarray`, default: `UP`
            Specifies the position of :attr:`__mob_index`.
        index_gap : :class:`float`, default: `0.25`
            Specifies the distance between :attr:`__mob_square` and :attr:`__mob_index`.
        label_pos : :class:`np.ndarray`, default: `LEFT`
            Specifies the position of :attr:`__mob_label`.
        label_gap : :class:`float`, default: `0.5`
            Specifies the distance between :attr:`__mob_square` and :attr:`__mob_label`
        next_to_mob : :class:`MArrayElement`, default: `None`
            Specifies placement for :attr:`__mob_square`.
        next_to_dir : :class:`np.ndarray`, default: `RIGHT`
            Specifies direction of placement for :attr:`__mob_square`.
        """

        super().__init__(**kwargs)

        # Initialize props
        self.__init_props(index_pos, index_gap, label_pos, label_gap)

        # Update props
        self.__update_props(
            mob_square_args, mob_value_args, mob_index_args, mob_label_args
        )

        # Initialize mobjects
        self.__init_mobs(True, True, True, True, next_to_mob, next_to_dir)

    def fetch_mob_square(self) -> Square:
        """Fetches the :class:`manim.Square` that represents the element body.

        Returns
        -------
        :class:`manim.Square`
            Represents the element body.
        """

        return self.__mob_square

    def fetch_mob_value(self) -> Text:
        """Fetches the :class:`manim.Text` that represents the element value.

        Returns
        -------
        :class:`manim.Text`
            Represents the element value.
        """

        return self.__mob_value

    def fetch_mob_index(self) -> Text:
        """Fetches the :class:`manim.Text` that represents the element index.

        Returns
        -------
        :class:`manim.Text`
            Represents the element index.
        """

        return self.__mob_index

    def fetch_mob_label(self) -> Text:
        """Fetches the :class:`manim.Text` that represents the element label.

        Returns
        -------
        :class:`manim.Text`
            Represents the element label.
        """

        return self.__mob_label

    def fetch_mob(self, mob_target: MArrayElementComp) -> Mobject:
        """Fetches :class:`manim.Mobject` based on enum :class:`m_enum.MArrayElementComp`.

        Parameters
        ----------
        mob_target : :class:`m_enum.MArrayElementComp`
            Specifies the component of :class:`MArrayElement` to fetch.

        Returns
        -------
        :class:`manim.Mobject`
            Represents the component of :class:`MArrayElement`.
        """

        if mob_target == MArrayElementComp.BODY:
            return self.fetch_mob_square()
        elif mob_target == MArrayElementComp.VALUE:
            return self.fetch_mob_value()
        elif mob_target == MArrayElementComp.INDEX:
            return self.fetch_mob_index()
        elif mob_target == MArrayElementComp.LABEL:
            return self.fetch_mob_label()
        else:
            return self

    def update_mob_value(self, mob_value_args: dict = {}) -> Text:
        """Re-intializes the :class:`manim.Text` that represents the element value.

        Parameters
        ----------
        mob_value_args : :class:`dict`, default: `{}`
            Arguments for :class:`manim.Text` that represents the element value.

        Returns
        -------
        :class:`manim.Text`
            Represents the updated element value.
        """

        self.__update_props(mob_value_args=mob_value_args)
        self.remove(self.__mob_value)
        self.__init_mobs(init_value=True)
        self.add(self.__mob_value)
        return self.__mob_value

    def update_mob_index(self, mob_index_args: dict = {}) -> Text:
        """Re-intializes the :class:`manim.Text` that represents the element index.

        Parameters
        ----------
        mob_index_args : :class:`dict`, default: `{}`
            Arguments for :class:`manim.Text` that represents the element index.

        Returns
        -------
        :class:`manim.Text`
            Represents the updated element index.
        """

        self.__update_props(mob_index_args=mob_index_args)
        self.remove(self.__mob_index)
        self.__init_mobs(init_index=True)
        self.add(self.__mob_index)
        return self.__mob_index

    def update_mob_label(self, mob_label_args: dict = {}) -> Text:
        """Re-intializes the :class:`manim.Text` that represents the element label.

        Parameters
        ----------
        mob_label_args : :class:`dict`, default: `{}`
            Arguments for :class:`manim.Text` that represents the element label.

        Returns
        -------
        :class:`manim.Text`
            Represents the updated element label.
        """

        self.__update_props(mob_label_args=mob_label_args)
        self.remove(self.__mob_label)
        self.__init_mobs(init_label=True)
        self.add(self.__mob_label)
        return self.__mob_label

    def animate_mob_square(self) -> "_AnimationBuilder":  # type: ignore
        """Invokes the :meth:`manim.Square.animate` property of :class:`manim.Square` for the element body.

        Returns
        -------
        :class:`_AnimationBuilder`
            Value returned by :meth:`manim.Square.animate` property of :class:`manim.Square`.
        """

        return self.__mob_square.animate

    def animate_mob_value(self) -> "_AnimationBuilder":  # type: ignore
        """Invokes the :meth:`manim.Text.animate` property of :class:`manim.Text` for the element value.

        Returns
        -------
        :class:`_AnimationBuilder`
            Value returned by :meth:`manim.Text.animate` property of :class:`manim.Text`.
        """

        return self.__mob_value.animate

    def animate_mob_index(self) -> "_AnimationBuilder":  # type: ignore
        """Invokes the :meth:`manim.Text.animate` property of :class:`manim.Text` for the element index.

        Returns
        -------
        :class:`_AnimationBuilder`
            Value returned by :meth:`manim.Text.animate` property of :class:`manim.Text`.
        """

        return self.__mob_index.animate

    def animate_mob_label(self) -> "_AnimationBuilder":  # type: ignore
        """Invokes the :meth:`manim.Text.animate` property of :class:`manim.Text` for the element label.

        Returns
        -------
        :class:`_AnimationBuilder`
            Value returned by :meth:`manim.Text.animate` property of :class:`manim.Text`.
        """

        return self.__mob_label.animate


